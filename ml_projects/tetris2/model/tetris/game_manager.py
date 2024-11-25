import numpy as np

from game_actions import Action

from .game_events import Event
from .grid import Grid
from .refill_queue import RefillingQueue
from .side_board import Manager, LevelManager, ScoreManger, TimeManager
from .tetromino import TetrominoShape, Tetromino

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
        self.board = board
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

        self.falling_tetromino: Tetromino

        self.held_tetromino: TetrominoShape
        self.can_use_held_tetromino: bool

        self.game_over: bool
        self.game_pause: bool

        self.reset()

    def reset(self):
        self.board.clear()
        self.tetromino_shape_queue.reset()

        for manager in self.managers:
            manager.reset()

        self.falling_tetromino = None

        self.held_tetromino = None
        self.can_use_held_tetromino = True

        self.game_over = False
        self.game_pause = False

    def get_board(self) -> np.ndarray:
        return self.board.get_grid_array()

    def get_current_piece_board(self) -> np.ndarray:
        grid = Grid.empty_like(self.board)
        if self.falling_tetromino is not None:
            grid.insert(
                self.falling_tetromino.get_position(),
                self.falling_tetromino.get_grid_array(),
            )
        return grid.get_grid_array()

    def get_piece_percent_placed(self) -> float:
        return 0

    def get_ghost_board(self) -> np.ndarray:
        empty_board = Grid.empty_like(self.board)

        if self.falling_tetromino is None:
            return empty_board.get_grid_array()

        ghost = self.falling_tetromino.copy()

        while not self.board.does_overlap(ghost.get_position(), ghost.get_grid_array()):
            ghost.move(dy=1)

        ghost.move(dy=-1)

        empty_board.insert(
            ghost.get_position(),
            ghost.get_grid_array(),
        )

        return empty_board.get_grid_array()

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
        return self.board.get_null_value()

    def get_next_falling_tetromino(
        self, tetromino_shape: TetrominoShape = None
    ) -> Tetromino:
        if tetromino_shape is None:
            tetromino_shape = self.tetromino_shape_queue.pop()

        tetromino_start_orientation = 0

        tetromino_start_x = (
            self.board.get_width()
            - tetromino_shape.get_width(tetromino_start_orientation)
        ) // 2

        tetromino_start_y = 0

        return Tetromino(
            tetromino_shape,
            (tetromino_start_x, tetromino_start_y),
            tetromino_start_orientation,
        )

    def change_x(self, dx: int) -> bool:

        if self.falling_tetromino is None:
            return False

        self.falling_tetromino.move(dx, 0)

        if self.board.does_overlap(
            self.falling_tetromino.get_position(),
            self.falling_tetromino.get_grid_array(),
        ):
            self.falling_tetromino.move(-dx, 0)
            return False

        return True

    def hard_drop(self) -> int:

        if self.falling_tetromino is None:
            return 0
        
        start_height = self.falling_tetromino.get_position()[1]

        while not self.board.does_overlap(
            self.falling_tetromino.get_position(),
            self.falling_tetromino.get_grid_array(),
        ):
            self.falling_tetromino.move(dy=1)
        self.falling_tetromino.move(dy=-1)

        self.board.insert(
            self.falling_tetromino.get_position(),
            self.falling_tetromino.get_grid_array(),
        )

        end_height = self.falling_tetromino.get_position()[1]

        self.falling_tetromino = None

        return end_height - start_height

    def hold(self) -> bool:
        if not self.can_use_held_tetromino:
            return False

        if self.held_tetromino is None:
            self.held_tetromino = self.falling_tetromino.shape
            self.falling_tetromino = self.get_next_falling_tetromino()
        else:
            self.falling_tetromino, self.held_tetromino = (
                self.get_next_falling_tetromino(self.held_tetromino),
                self.falling_tetromino.shape,
            )

        self.can_use_held_tetromino = False

        return True

    def rotate(self, rotations: int) -> bool:

        if self.falling_tetromino is None:
            return False

        for dx, dy in self.wall_kick_positions:
            self.falling_tetromino.move(dx, dy)

            old_orientation = self.falling_tetromino.orientation
            self.falling_tetromino.rotate(rotations)
            if self.board.does_overlap(
                self.falling_tetromino.get_position(),
                self.falling_tetromino.get_grid_array(),
            ):
                self.falling_tetromino.orientation = old_orientation
            else:
                return True

            self.falling_tetromino.move(-dx, -dy)

        return False

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

        if self.falling_tetromino is None:
            self.can_use_held_tetromino = True
            self.falling_tetromino = self.get_next_falling_tetromino()
        
        if self.board.does_overlap(
            self.falling_tetromino.get_position(),
            self.falling_tetromino.get_grid_array(),
        ):
            self.game_over = True
            self.board.insert(
                self.falling_tetromino.get_position(),
                self.falling_tetromino.get_grid_array(),
            )
            self.falling_tetromino = None

        do_soft_drop = False
        did_drop = False
        hard_drop_distance = 0

        for action in actions:
            match action:
                case Action.LEFT: self.change_x(-1)
                case Action.RIGHT: self.change_x(1)
                case Action.SPIN: self.rotate(1)
                case Action.SOFT_DROP: do_soft_drop = True
                case Action.HARD_DROP: hard_drop_distance = self.hard_drop()
                case Action.HOLD: self.hold()

        if self.falling_tetromino is not None:
            if self.time_manager.get_frame() % int(self.level_manager.get_drop_interval_seconds() * self.time_manager.get_fps() / (20 if do_soft_drop else 1)) == 0:
                self.falling_tetromino.move(dy=1)
                did_drop = True

            did_collide = self.board.does_overlap(
                self.falling_tetromino.get_position(),
                self.falling_tetromino.get_grid_array(),
            )

            if did_collide:
                self.falling_tetromino.move(dy=-1)
                did_collide = self.board.insert(
                    self.falling_tetromino.get_position(),
                    self.falling_tetromino.get_grid_array(),
                )
                self.falling_tetromino = None

        fulls_lines = self.board.find_full_lines()
        self.board.remove_full_lines(fulls_lines)

        for manager in self.managers:
            manager.handle_event({Event.SOFT_DROP: did_drop and do_soft_drop, Event.HARD_DROP: hard_drop_distance, Event.LINE_CLEAR: len(fulls_lines)})

        self.time_manager.tick()