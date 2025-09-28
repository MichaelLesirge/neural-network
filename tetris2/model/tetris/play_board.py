import numpy as np

from game_actions import Action

from .grid import Grid
from .tetromino import Tetromino

CoordinatePair = tuple[int, int]

class PlayBoard:
    def __init__(
        self,
        board: Grid,
        rotate_kick_positions: list[CoordinatePair] = None,
    ) -> None:
        self.board = board
        self.wall_kick_positions = rotate_kick_positions or [(0, 0)]

        self.falling_tetromino: Tetromino = None

    def reset(self) -> None:
        self.board.clear()

        self.falling_tetromino = None

    def copy(self) -> "PlayBoard":
        play_board = PlayBoard(self.board.copy(), self.wall_kick_positions)
        play_board.set_falling_tetromino(self.falling_tetromino.copy())
        return play_board
    
    def get_grid(self) -> Grid:
        return self.board

    def get_current_piece_board(self) -> np.ndarray:
        grid = Grid.empty_like(self.board)

        if self.falling_tetromino is not None:
            grid.insert(
                self.falling_tetromino.get_position(),
                self.falling_tetromino.get_grid_array(),
            )

        return grid.get_grid_array()

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
    
    def get_array_null_value(self) -> int:
        return self.board.get_null_value()

    def change_x(self, dx: int) -> bool:

        if self.falling_tetromino is None:
            return False

        self.falling_tetromino.move(dx, 0)

        if self.is_overlapping():
            self.falling_tetromino.move(-dx, 0)
            return False

        return True

    def rotate(self, rotations: int) -> bool:

        if self.falling_tetromino is None:
            return False

        for dx, dy in self.wall_kick_positions:
            self.falling_tetromino.move(dx, dy)

            old_orientation = self.falling_tetromino.orientation

            self.falling_tetromino.rotate(rotations)

            if self.is_overlapping():
                self.falling_tetromino.orientation = old_orientation
            else:
                return True

            self.falling_tetromino.move(-dx, -dy)

        return False

    def hard_drop(self) -> int:

        if self.falling_tetromino is None:
            return 0
        
        distance = 0

        while self.soft_drop():
            distance += 1

        self.freeze()

        return distance
    
    def soft_drop(self) -> bool:
            
        if self.falling_tetromino is None:
            return False

        self.falling_tetromino.move(dy=1)

        if self.is_overlapping():
            self.falling_tetromino.move(dy=-1)
            return False

        return True
 
    def get_falling_tetromino(self) -> Tetromino:
        return self.falling_tetromino

    def set_falling_tetromino(self, tetromino: Tetromino) -> None:
        self.falling_tetromino = tetromino

    def has_falling_tetromino(self) -> bool:
        return self.falling_tetromino is not None

    def is_overlapping(self) -> bool:
        if self.falling_tetromino is None:
            return False
        return self.board.does_overlap(
            self.falling_tetromino.get_position(),
            self.falling_tetromino.get_grid_array())
    
    def is_over_blocks(self) -> bool:
        if self.falling_tetromino is None:
            return False

        x, y = self.falling_tetromino.get_position()
        
        return self.board.does_overlap(
            (x, y + 1),
            self.falling_tetromino.get_grid_array()
        )

    def freeze(self) -> bool:

        if self.falling_tetromino is None:
            return False

        self.board.insert(
            self.falling_tetromino.get_position(),
            self.falling_tetromino.get_grid_array(),
        )

        self.falling_tetromino = None

        return True
     
    def __str__(self) -> str:
        copy = self.board.copy()
        if self.falling_tetromino is not None:
            copy.insert(
                self.falling_tetromino.get_position(),
                self.falling_tetromino.get_grid_array(),
            )
        return str(copy)