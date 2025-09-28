import numpy as np

from . import tetris_website
from model import TetrominoShape, Tetromino, Grid, PlayBoard
from game_actions import Action

# Tetris.com

def hash_array(array: np.ndarray) -> int:
    return hash((array.tobytes(), array.shape))

class TetrisWebsiteGame:
    def __init__(self, shapes: list[TetrominoShape], null_value: int = 0) -> None:        
        self.shape_key: dict[np.ndarray, tuple[TetrominoShape, int]] = {}
        for shape in shapes:
            for i in range(TetrominoShape.MAX_ORIENTATIONS):
                self.shape_key[hash_array(shape.get_thumbnail_grid_array(orientation=i) != null_value)] = (shape, i)
        
        self.last_piece = Tetromino()
    
    def setup(self):
        tetris_website.setup()
    
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

    def get_board(self) -> np.ndarray:
        return self.board
    
    def get_piece_board(self) -> np.ndarray:
        return self.piece_board
    
    def update(self, actions: list[Action]) -> None:

        board = tetris_website.get_board()

        piece = self.extract_tetromino(board, expect_orientation=self.last_piece.get_orientation())

        if piece.get_name() == "Unknown":
            piece = self.last_piece

        grid = Grid(board, null_value=0)

        grid.insert_empty(
            piece.get_grid_array(),
            piece.get_position(),
        )

        play_board = PlayBoard(grid)

        self.board = grid.get_grid_array()

        for action in actions:
            match action:
                case Action.LEFT:
                    tetris_website.left()
                    play_board.change_x(-1)
                case Action.RIGHT:
                    tetris_website.right()
                    play_board.change_x(1)
                case Action.SPIN:
                    tetris_website.rotate()
                    play_board.rotate(1)
                case Action.SOFT_DROP:
                    tetris_website.soft_drop()
                case Action.HARD_DROP:
                    tetris_website.hard_drop()
                    play_board.hard_drop()
                case Action.HOLD:
                    tetris_website.hold()

        self.last_piece = play_board.get_falling_tetromino


