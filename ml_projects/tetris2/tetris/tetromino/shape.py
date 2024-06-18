import numpy as np
from numpy.typing import NDArray

N = np.uint8


def rotate(grid: np.ndarray) -> np.ndarray:
    return np.flip(np.rot90(grid))


class TetrominoShape:
    MAX_ORIENTATIONS = 4

    def __init__(self, name_char: str, shape: NDArray, empty: N = 0) -> None:

        self.key = ord(name_char)
        self.empty = empty

        shape_array = np.where(shape, self.key, self.empty).astype(N)

        self.orientations: list[np.ndarray] = []

        for i in range(TetrominoShape.MAX_ORIENTATIONS):
            self.orientations.append(shape_array)
            shape_array = rotate(shape_array)

            if np.array_equal(shape_array, self.orientations[0]):
                break

    def get_name(self) -> str:
        return chr(self.key)

    def get_grid_array(self, orientation=0) -> np.ndarray:
        return self.orientations[orientation]

    def get_width(self, orientation=0) -> int:
        return self.get_grid_array(orientation).shape[1]

    def get_height(self, orientation=0) -> int:
        return self.get_grid_array(orientation).shape[0]

    def get_thumbnail_grid_array(self) -> np.ndarray:
        grid = self.get_grid_array(0)

        empty_positions = np.where(grid != self.empty)
        trimmed_grid = grid[
            min(empty_positions[0]) : max(empty_positions[0]) + 1,
            min(empty_positions[1]) : max(empty_positions[1]) + 1,
        ]

        return trimmed_grid

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.get_name()}, {self.get_grid_array()})"
