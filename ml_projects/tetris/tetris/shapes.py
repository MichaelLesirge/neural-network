import numpy as np


def rotate(shape):
    return np.flip(np.rot90(shape))

class TetrominoShape:
    MAX_ORIENTATIONS = 4
    
    ALL_SHAPES: list["TetrominoShape"] = []
    SHAPE_ID_MAP: dict[int, "TetrominoShape"] = {}

    def __init__(self, name: str, shape: list[list[int]] | np.ndarray, color: str | tuple[int, int, int] = "white") -> None:

        self.name = name
        self.color = color
        self.id = len(self.SHAPE_ID_MAP) + 1
        
        TetrominoShape.ALL_SHAPES.append(self)
        TetrominoShape.SHAPE_ID_MAP[self.id] = self

        shape = np.array(shape, dtype=np.uint8)

        self.orientations: list[np.ndarray] = []
        for i in range(TetrominoShape.MAX_ORIENTATIONS):
            self.orientations.append(shape)
            shape = rotate(shape)
            if np.array_equal(shape, self.orientations[0]):
                break

    def get_name(self) -> str: return self.name

    def get_color(self) -> str | tuple[int, int, int]: return self.color

    def get_id(self) -> int: return self.id

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


I = TetrominoShape("I", [
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
], (0, 240, 240))

O = TetrominoShape("O", [
    [1, 1],
    [1, 1],
], (240, 240, 0))

L = TetrominoShape("L", [
    [0, 0, 1],
    [1, 1, 1],
    [0, 0, 0],
], (240, 160, 0))

J = TetrominoShape("J", [
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 0],
], (0, 0, 240))

T = TetrominoShape("T", [
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0],
], (160, 0, 240))

Z = TetrominoShape("Z", [
    [1, 1, 0],
    [0, 1, 1],
    [0, 0, 0],
], (240, 0, 0))

S = TetrominoShape("S", [
    [0, 1, 1],
    [1, 1, 0],
    [0, 0, 0],
], (0, 240, 0))

def main() -> None:
    states = [" .", "██"]

    for shape in TetrominoShape.ALL_SHAPES:
        print(shape.name + ": ")
        for i, orientation in enumerate(shape.rotations):
            print()
            print("\n".join(
                "".join(states[value] for value in row) for row in orientation
            ))
        print()


if __name__ == "__main__":
    main()
