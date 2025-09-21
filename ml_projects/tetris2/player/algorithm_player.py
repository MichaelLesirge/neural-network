import itertools

import numpy as np

from game_actions import Action
from game_state import State
from .player import Player
from model import Grid, PlayBoard, Tetromino, TetrominoShape

def hash_array(array: np.ndarray) -> int:
    return hash((array.tobytes(), array.shape))

class AlgorithmPlayer(Player):
    def __init__(self, shapes: list[TetrominoShape], null_value: int = 0) -> None:
        self.base_move_possibilities_cache: dict[int, list[Action]] = {}
        self.shape_key: dict[np.ndarray, tuple[TetrominoShape, int]] = {}
        for shape in shapes:
            for i in range(TetrominoShape.MAX_ORIENTATIONS):
                self.shape_key[hash_array(shape.get_thumbnail_grid_array(orientation=i) != null_value)] = (shape, i)
        self.cache = {}
        self.expected_orientation = {}

    def get_name(self) -> str:
        return "Algorithm Player"
    
    def moves_to_str(self, moves: list[Action]) -> None:
        map = {Action.LEFT: "L", Action.RIGHT: "R", Action.SOFT_DROP: "-", Action.HARD_DROP: ".", Action.SPIN: "S", Action.NONE: "_", Action.HOLD: "H"}
        return "".join(map[move] for move in moves)

    def extract_tetromino(self, board: np.ndarray, expect_orientation: int = None, null_value: int = 0) -> Tetromino:
        empty_positions = np.where(board != null_value)

        if any(position.size == 0 for position in empty_positions):
            return None

        row = min(empty_positions[0])
        col = min(empty_positions[1])

        trimmed_board = board[
            row : max(empty_positions[0]) + 1,
            col : max(empty_positions[1]) + 1,
        ]

        shape, orientation = self.shape_key.get(hash_array(trimmed_board != null_value), (TetrominoShape("Unknown", None, trimmed_board, null_value), 0))
        if expect_orientation is not None:
            orientation = expect_orientation % TetrominoShape.MAX_ORIENTATIONS
        
        empty_positions_in_shape = np.where(shape.get_grid_array(orientation) != null_value)
        row_offset = min(empty_positions_in_shape[0])
        col_offset = min(empty_positions_in_shape[1])

        # print(shape.get_name(), (col, row), (col_offset, row_offset), orientation)

        return Tetromino(
            shape,
            (col - col_offset, row - row_offset),
            orientation,
        )

    def get_penalty(self, grid: Grid, lines_removed = None) -> float:
        heights = grid.get_column_heights()

        holes = grid.get_number_of_holes()
        unfixableHoles = grid.get_number_of_surrounded_holes()
        max_height = max(heights)
        avg_height = sum(heights) / len(heights)
        bumpiness = grid.get_heights_bumpiness()

        full_lines = lines_removed or len(grid.find_full_lines())

        return (
            -(2 ** full_lines * 5)
            + 2 * unfixableHoles
            + 15 * holes
            + 5 * (avg_height ** 1.25)
            + 2 * max_height
            + 0.1 * bumpiness
            + (max_height > 17) * 50
            + 0
        )

    def generate_base_moves(self, grid: Grid) -> list[list[Action]]:
        height, width = grid.get_grid_array().shape
        if width not in self.base_move_possibilities_cache:
            options = [
                [Action.LEFT if i < x else Action.NONE for i in range(width)] + [Action.NONE] * (height - width)
                for x in range(width + 1)
            ] + [
                [Action.RIGHT if i <= x else Action.NONE for i in range(width)] + [Action.NONE] * (height - width)
                for x in range(width)
            ]
            self.base_move_possibilities_cache[width] = []
            for i in range(4):
                self.base_move_possibilities_cache[width].extend([Action.SPIN] * i + (option[:-i] or option) for option in options)
            # print("\n".join(self.moves_to_str(moves) for moves in self.base_move_possibilities_cache[width]))
        return self.base_move_possibilities_cache[width]
    
    def generate_deep_explore_moves(self, grid: Grid, n = 3) -> list[list[Action]]:
        return itertools.product(
            [Action.LEFT, Action.RIGHT, Action.SPIN, Action.NONE], repeat=n
        )


    def get_actions(self, state: State) -> list[Action]:

        grid = Grid(state.board.copy(), state.board_null_value)
        board_hash = hash_array(grid.get_grid_array())

        tetromino = self.extract_tetromino(
            state.current_tetromino_board, self.expected_orientation.get(board_hash, 0), state.board_null_value
        )

        play_board = PlayBoard(grid)        

        if tetromino is not None:
            play_board.set_falling_tetromino(tetromino)
        else:
            return []

        start_height = play_board.get_falling_tetromino().get_position()[1]

        if board_hash not in self.cache or start_height not in self.cache[board_hash]: 
            lowest_penalty = float("inf")
            lowest_penalty_moves = []
            
            lowest_penalty_end_height = start_height

            for base_moves in self.generate_base_moves(grid):
                play_board_with_base = play_board.copy()
                used_base_moves = []
                for base_move in base_moves:
                    match base_move:
                        case Action.LEFT:
                            play_board_with_base.change_x(-1)
                        case Action.RIGHT:
                            play_board_with_base.change_x(1)
                    used_base_moves.append(base_move) 
                    if not play_board_with_base.soft_drop():
                        break
                
                play_board_with_base.hard_drop()
                play_board_with_base.freeze()

                
                for deep_moves in self.generate_deep_explore_moves(grid, max(min(3, play_board.get_grid().get_number_of_holes()), 1)):
                    moves = used_base_moves[:-len(deep_moves)] + list(deep_moves)
                    used_moves = []
                    play_board_with_deep_moves = play_board.copy()
                    for move in moves:
                        match move:
                            case Action.LEFT:
                                play_board_with_deep_moves.change_x(-1)
                            case Action.RIGHT:
                                play_board_with_deep_moves.change_x(1)
                            case Action.SPIN:
                                play_board_with_deep_moves.rotate(1)
                        used_moves.append(move)
                        if not play_board_with_deep_moves.soft_drop():
                            break

                    end_height = play_board_with_deep_moves.get_falling_tetromino().get_position()[1]

                    play_board_with_deep_moves.hard_drop()
                    play_board_with_deep_moves.freeze()

                    full_lines = play_board_with_deep_moves.get_grid().find_full_lines()
                    play_board_with_deep_moves.get_grid().remove_full_lines(full_lines)

                    while len(used_moves) > 0 and used_moves[-1] in (Action.NONE, Action.SOFT_DROP):
                        used_moves.pop()
                    used_moves.append(Action.HARD_DROP)

                    penalty = self.get_penalty(play_board_with_deep_moves.get_grid(), lines_removed=len(full_lines))
                    if lowest_penalty > penalty or (lowest_penalty == penalty and len(used_moves) < len(lowest_penalty_moves)):
                        lowest_penalty = penalty
                        lowest_penalty_moves = used_moves
                        lowest_penalty_end_height = end_height
            
            if lowest_penalty > self.get_penalty(play_board.get_grid()) + 20 and state.can_use_held_tetromino:
                lowest_penalty_moves = [Action.HOLD]
                
            self.cache[board_hash] = {height: [move] for height, move in zip(range(start_height, lowest_penalty_end_height + 1), lowest_penalty_moves)}

        for key in list(self.cache.keys()):
            if key != board_hash:
                del self.cache[key]

        if start_height in self.cache[board_hash]:
            result = self.cache[board_hash][start_height]
            if result == [Action.SPIN]:
                self.expected_orientation[board_hash] = (self.expected_orientation.get(board_hash, 0) + 1) % TetrominoShape.MAX_ORIENTATIONS
            return [result.pop()] if len(result) > 0 else [Action.SOFT_DROP]
        

        
