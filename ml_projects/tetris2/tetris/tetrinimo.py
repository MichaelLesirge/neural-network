import numpy as np
from typing import Generator

class TetrominoShape:
    MAX_ORIENTATIONS = 4

    def __init__(self, name: str, shape: list[list[int]] | np.ndarray) -> None:

        self.name = name

        shape = np.array(shape, dtype=np.uint8)

        self.orientations: list[np.ndarray] = []
        for i in range(TetrominoShape.MAX_ORIENTATIONS):
            self.orientations.append(shape)
            shape = np.flip(np.rot90(shape))(shape)
            if np.array_equal(shape, self.orientations[0]):
                break

    def get_name(self) -> str: return self.name

    def get_num_of_orientations(self) -> int: return len(self.orientations)
    
    def get_grid(self, orientation = 0) -> np.ndarray: return self.orientations[orientation]
    
    def get_width(self, orientation = 0) -> int: return self.get_grid(orientation).shape[1]
    
    def get_height(self, orientation = 0) -> int: return self.get_grid(orientation).shape[0]

    def get_trimmed_grid(self, orientation = 0):
        grid = self.get_grid(orientation) 
        
        zeros = np.where(grid != 0)
        grid = grid[min(zeros[0]) : max(zeros[0]) + 1, min(zeros[1]) : max(zeros[1]) + 1]
        
        return grid
        
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.orientations[0]})"

class FallingTetromino:
    def __init__(self, x: int, y: int, shape: TetrominoShape, orientation: int = 0) -> None:
        self.x = x
        self.y = y
        
        self.shape = shape
        
        self.orientation = orientation % len(self.shape.orientations)
    
    def get_height(self) -> int: return self.get_grid().shape[1]
        
    def get_width(self) -> int: return self.get_grid().shape[0]

    def get_name(self) -> str: return self.shape.get_name()
    
    def get_grid(self) -> np.ndarray[np.uint8]: return self.shape.get_grid(self.orientation)
     
    def rotate(self) -> None: self.orientation = (self.orientation + 1) % len(self.shape.orientations)
            
    def copy(self) -> "FallingTetromino": return FallingTetromino(self.x, self.y, self.shape, self.orientation)

    def __iter__(self) -> Generator[tuple[np.uint8, tuple[int, int]]]:
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                yield (self.get_grid()[row][col], (self.y + row, self.x + col))
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, shape={self.shape}, orientation={self.orientation})"