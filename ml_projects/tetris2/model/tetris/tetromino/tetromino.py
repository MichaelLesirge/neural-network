from typing import Generator, Self

import numpy as np

from .shape import TetrominoShape

CoordinatePair = tuple[int, int]


class Tetromino:
    def __init__(
        self,
        shape: TetrominoShape,
        start_position: CoordinatePair = (0, 0),
        orientation: int = 0,
    ) -> None:
        self.shape = shape

        self.goto(start_position)
        self.set_orientation(orientation)

    def get_name(self) -> str:
        return self.shape.get_name()

    def get_height(self) -> int:
        return self.get_grid_array().shape[1]

    def get_width(self) -> int:
        return self.get_grid_array().shape[0]

    def get_grid_array(self) -> np.ndarray:
        return self.shape.get_grid_array(self.orientation)

    def get_position(self) -> CoordinatePair:
        return (self.x, self.y)

    def goto(self, position: CoordinatePair) -> int:
        self.x, self.y = position

    def move(self, dx=0, dy=0) -> int:
        self.x += dx
        self.y += dy

    def rotate(self, rotations = 1) -> None:
        self.set_orientation(self.orientation + rotations)

    def set_orientation(self, orientation: int) -> int:
        self.orientation = orientation % len(self.shape.orientations)

    def copy(self) -> Self:
        return self.__class__(self.shape, (self.x, self.y), self.orientation)

    def __iter__(self) -> Generator[tuple[int, CoordinatePair], None, None]:
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                yield (self.get_grid_array()[row][col], (self.y + row, self.x + col))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, shape={self.shape}, orientation={self.orientation})"
