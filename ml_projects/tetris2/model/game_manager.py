import numpy as np

from game_actions import Action
from game_state import State

from .tetris.game_events import Event
from .tetris.grid import Grid
from .tetris.refill_queue import RefillingQueue
from .tetris.side_board import Manager, LevelManager, ScoreManger, TimeManager
from .tetris.tetromino import TetrominoShape, Tetromino
from .tetris.play_board import PlayBoard

CoordinatePair = tuple[int, int]

class TetrisGameManager:
    def __init__(
        self,
        board: Grid,
        tetromino_shape_queue: RefillingQueue[TetrominoShape],
        level_manager: LevelManager,
        score_manager: ScoreManger,
        time_manager: TimeManager,
        rotate_kick_positions: list[CoordinatePair],
    ) -> None:
        self.tetromino_shape_queue = tetromino_shape_queue
        self.level_manager = level_manager
        self.score_manager = score_manager
        self.time_manager = time_manager
        self.wall_kick_positions = rotate_kick_positions

        self.managers: list[Manager] = [
            self.level_manager,
            self.score_manager,
            self.time_manager,
        ]

        self.held_tetromino: TetrominoShape
        self.can_use_held_tetromino: bool

        self.game_over: bool
        self.game_pause: bool

        self.time_till_next_drop: int
        self.time_till_freeze: int

        self.play_board = PlayBoard(board, rotate_kick_positions=self.wall_kick_positions)

        self.reset()

    def reset(self):
        self.play_board.reset()
        self.tetromino_shape_queue.reset()

        for manager in self.managers:
            manager.reset()

        self.held_tetromino = None
        self.can_use_held_tetromino = True

        self.game_over = False
        self.game_pause = False

        self.time_till_next_drop = 0
        self.time_till_freeze = None

    def get_board(self) -> np.ndarray:
        return self.play_board.get_grid().get_grid_array()

    def get_current_piece_board(self) -> np.ndarray:
        return self.play_board.get_current_piece_board()

    def get_ghost_board(self) -> np.ndarray:
        return self.play_board.get_ghost_board()

    def get_piece_percent_placed(self) -> float:
        if self.time_till_freeze is None:
            return 0
        return self.time_till_freeze / self.level_manager.get_drop_interval_seconds()

    def get_held_tetromino(self) -> np.ndarray | None:
        if self.held_tetromino is None:
            return None

        return self.held_tetromino.get_thumbnail_grid_array()

    def get_can_use_held_tetromino(self) -> bool:
        return self.can_use_held_tetromino

    def get_tetromino_queue(self) -> list[np.ndarray]:
        return [
            shape.get_thumbnail_grid_array()
            for shape in self.tetromino_shape_queue.view()
        ]

    def get_array_null_value(self) -> int:
        return self.play_board.get_array_null_value()
    
    def set_falling_tetromino_shape(self, tetromino: TetrominoShape) -> None:
        self.play_board.set_falling_tetromino(self.create_falling_tetromino(tetromino))
        
        self.can_use_held_tetromino = True
        self.time_till_next_drop = self.level_manager.get_drop_interval_seconds()
        self.time_till_freeze = None

    def create_falling_tetromino(
        self, tetromino_shape: TetrominoShape
    ) -> Tetromino:

        tetromino_start_orientation = 0

        tetromino_start_x = (
            self.play_board.board.get_width()
            - tetromino_shape.get_width(tetromino_start_orientation)
        ) // 2

        tetromino_start_y = 0

        return Tetromino(
            tetromino_shape,
            (tetromino_start_x, tetromino_start_y),
            tetromino_start_orientation,
        )

    def hold(self) -> bool:
        if not self.can_use_held_tetromino:
            return False

        next_tetromino_shape = self.tetromino_shape_queue.pop() if self.held_tetromino is None else self.held_tetromino

        self.held_tetromino = self.play_board.get_falling_tetromino().get_shape_type()

        self.set_falling_tetromino_shape(next_tetromino_shape)

        self.can_use_held_tetromino = False

        return True

    def get_sidebar_info(self) -> dict[str, str]:
        return {
            "score": str(self.score_manager.get_score()),
            "level": str(self.level_manager.get_level()),
            "lines": str(self.score_manager.get_lines_cleared()),
            "time": self.time_manager.get_time_str(),
        }
    
    def is_game_over(self) -> bool:
        return self.game_over
    
    def pause(self) -> None:
        self.game_pause = True

    def unpause(self) -> None:
        self.game_pause = False
    
    def is_game_paused(self) -> bool:
        return self.game_pause

    def step(self, actions: list[Action]):
        if self.game_over or self.game_pause:
            return

        if not self.play_board.has_falling_tetromino():
            self.set_falling_tetromino_shape(self.tetromino_shape_queue.pop())
        
        if self.play_board.is_overlapping():
            self.game_over = True
            self.play_board.freeze()
            self.falling_tetromino = None

        do_soft_drop = False
        did_drop = False
        hard_drop_distance = 0

        for action in actions:
            match action:
                case Action.LEFT: self.play_board.change_x(-1)
                case Action.RIGHT: self.play_board.change_x(1)
                case Action.SPIN: self.play_board.rotate(1)
                case Action.SOFT_DROP: do_soft_drop = True
                case Action.HARD_DROP: hard_drop_distance = self.play_board.hard_drop()
                case Action.HOLD: self.hold()

        if self.play_board.has_falling_tetromino():

            did_collide = self.play_board.is_over_blocks()

            if did_collide:
                if self.time_till_freeze is None:
                    self.time_till_freeze = self.level_manager.get_drop_interval_seconds()
                elif self.time_till_freeze <= 0:
                    self.play_board.freeze()
                else:
                    self.time_till_freeze -= 1 / self.time_manager.get_fps()

            elif self.time_till_next_drop <= 0:
                self.play_board.soft_drop()
                did_drop = True
                self.time_till_next_drop = self.level_manager.get_drop_interval_seconds()

            else:
                self.time_till_freeze = None

            self.time_till_next_drop -= (1 / self.time_manager.get_fps()) * (20 if do_soft_drop else 1)

        fulls_lines = self.play_board.get_grid().find_full_lines()
        self.play_board.get_grid().remove_full_lines(fulls_lines)

        for manager in self.managers:
            manager.handle_event({Event.SOFT_DROP: did_drop and do_soft_drop, Event.HARD_DROP: hard_drop_distance, Event.LINE_CLEAR: len(fulls_lines)})

        self.time_manager.tick()