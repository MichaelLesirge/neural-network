import enum

from .grid import Grid
from .refill_queue import RefillingQueue
from .tetromino import TetrominoShape, Tetromino


class Move(enum.Enum):
    SPIN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()
    SOFT_DROP = enum.auto()
    HARD_DROP = enum.auto()
    HOLD = enum.auto()

    QUIT = enum.auto()


# Model
class TetrisGameManager:
    def __init__(
        self, board: Grid, tetromino_shape_queue: RefillingQueue[TetrominoShape]
    ) -> None:
        self.board = board
        self.tetromino_shape_queue = tetromino_shape_queue
        self.falling_tetromino = None

    def reset(self):
        self.board.clear()
        self.tetromino_shape_queue.reset()
        self.falling_tetromino = None

    def _get_next_falling_tetromino(self) -> Tetromino:
        tetromino_shape = self.tetromino_shape_queue.pop()

        tetromino_start_orientation = 0
        tetromino_start_position = (
            (
                self.board.get_width()
                - tetromino_shape.get_width(tetromino_start_orientation)
            )
            // 2,
            0,
        )

        return Tetromino(
            tetromino_shape, tetromino_start_position, tetromino_start_orientation
        )

    def step(self, actions: list[Move]):
        if self.falling_tetromino is None:
            self.falling_tetromino = self._get_next_falling_tetromino()

        self.falling_tetromino.move(dy=1)
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
