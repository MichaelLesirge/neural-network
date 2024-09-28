import numpy as np

from game_actions import Action

from .grid import Grid
from .refill_queue import RefillingQueue
from .tetromino import TetrominoShape, Tetromino

# Model


class TetrisGameManager:
    def __init__(
        self, board: Grid, tetromino_shape_queue: RefillingQueue[TetrominoShape]
    ) -> None:
        self.board = board
        self.tetromino_shape_queue = tetromino_shape_queue
        self.falling_tetromino: Tetromino = None
        self.held_tetromino: Tetromino = None

    def reset(self):
        self.board.clear()
        self.tetromino_shape_queue.reset()
        self.falling_tetromino = None

        self.frame = 0

    def get_board(self) -> np.ndarray:
        return self.board.get_grid_array()

    def get_current_piece_board(self) -> np.ndarray:
        grid = Grid.empty_like(self.board)
        if self.falling_tetromino is not None:
            grid.insert(self.falling_tetromino.get_position(),
                        self.falling_tetromino.get_grid_array())
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
            self.falling_tetromino.get_position(),
            self.falling_tetromino.get_grid_array(),
        )

        return empty_board.get_grid_array()

    def get_held_tetromino(self) -> np.ndarray | None:
        if self.held_tetromino is None:
            return None

        return self.held_tetromino.get_grid_array()

    def can_use_held_tetromino(self) -> bool:
        return False

    def get_tetromino_queue(self) -> list[np.ndarray]:
        return [shape.get_grid_array() for shape in self.tetromino_shape_queue.view()]

    def get_array_null_value(self) -> int:
        return self.board.get_null_value()

    def _get_next_falling_tetromino(self) -> Tetromino:
        tetromino_shape = self.tetromino_shape_queue.pop()

        tetromino_start_orientation = 0

        tetromino_start_x = (
            self.board.get_width()
            - tetromino_shape.get_width(tetromino_start_orientation)
        ) // 2

        tetromino_start_y = 0

        return Tetromino(
            tetromino_shape, (tetromino_start_x,
                              tetromino_start_y), tetromino_start_orientation
        )

    def change_x(self, dx: int) -> bool:
                
        self.falling_tetromino.move(dx, 0)
        
        if self.board.does_overlap(self.falling_tetromino.get_position(), self.falling_tetromino.get_grid_array()):
            self.falling_tetromino.move(-dx, 0)
            return False
        
        return True

    def rotate(self, rotations: int) -> bool:

        positions_to_try = [(0, 0)]

        if True:
            positions_to_try.extend([(1, 0), (-1, 0)])

        for (dx, dy) in positions_to_try:
            self.falling_tetromino.move(dx, dy)

            old_orientation = self.falling_tetromino.orientation
            self.falling_tetromino.rotate(rotations)
            if self.board.does_overlap(self.falling_tetromino.get_position(), self.falling_tetromino.get_grid_array()):
                self.falling_tetromino.orientation = old_orientation
            else:
                return True

            self.falling_tetromino.move(-dx, -dy)
        
        return False

    def step(self, actions: list[Action]):
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

        for action in actions:
            match action:
                case Action.LEFT: self.change_x(-1)
                case Action.RIGHT: self.change_x(1)
                case Action.SPIN: self.rotate(1)
