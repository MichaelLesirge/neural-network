import numpy as np
from display import Color

def rotate(grid: np.ndarray) -> np.ndarray:
    return np.flip(np.rot90(grid))


class TetrominoShape:
    MAX_ORIENTATIONS = 4

    def __init__(self, name: str, color: Color, shape: np.ndarray, null_value = 0) -> None:

        self.name = name
        self.color = color

        self.bytes = np.array(shape).tobytes()

        self.null_value = null_value

        shape_array = np.where(shape, hash(self), self.null_value)

        self.orientations: list[np.ndarray] = []

        for i in range(TetrominoShape.MAX_ORIENTATIONS):
            self.orientations.append(shape_array)
            shape_array = rotate(shape_array)

            if np.array_equal(shape_array, self.orientations[0]):
                break
        
    def get_name(self) -> str:
        return self.name
    
    def get_color(self) -> Color:
        return self.color

    def get_grid_array(self, orientation=0) -> np.ndarray:
        return self.orientations[orientation % len(self.orientations)]

    def get_width(self, orientation=0) -> int:
        return self.get_grid_array(orientation).shape[1]

    def get_height(self, orientation=0) -> int:
        return self.get_grid_array(orientation).shape[0]

    def get_thumbnail_grid_array(self, orientation=0) -> np.ndarray:
        grid = self.get_grid_array(orientation)

        empty_positions = np.where(grid != self.null_value)
        trimmed_grid = grid[
            min(empty_positions[0]) : max(empty_positions[0]) + 1,
            min(empty_positions[1]) : max(empty_positions[1]) + 1,
        ]

        return trimmed_grid

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.get_name()}, {self.get_grid_array()})"

    def __hash__(self) -> int:
        return hash((self.get_name(), self.bytes)) % 2**16