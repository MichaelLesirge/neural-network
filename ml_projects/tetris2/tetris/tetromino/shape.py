import numpy as np
from numpy.typing import NDArray

def rotate(grid: np.ndarray) -> np.ndarray:
    return np.flip(np.rot90(grid))

class TetrominoShape:
    MAX_ORIENTATIONS = 4

    def __init__(self, name_char: str, shape: NDArray, empty: int = 0) -> None:

        self.name = ord(name_char)
        self.empty = empty
                
        shape_array = np.where(shape, self.name, self.empty).astype(int)
        
        self.orientations: list[np.ndarray] = []
        for i in range(TetrominoShape.MAX_ORIENTATIONS):
            self.orientations.append(shape_array)
            shape_array = rotate(shape_array)
            if np.array_equal(shape_array, self.orientations[0]):
                break

    def get_name(self) -> str:
        return chr(self.name)
    
    def get_grid_array(self, orientation = 0) -> np.ndarray:
        return self.orientations[orientation]
    
    def get_width(self, orientation = 0) -> int:
        return self.get_grid_array(orientation).shape[1]
    
    def get_height(self, orientation = 0) -> int:
        return self.get_grid_array(orientation).shape[0]
 
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.get_name()}, {self.get_grid_array()})"