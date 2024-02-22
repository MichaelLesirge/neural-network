import numpy as np


def rotate(shape):
    return np.flip(np.rot90(shape))

class TetrominoShape:
    MAX_ROTATIONS = 4
    
    ALL_SHAPES: list["TetrominoShape"] = []
    SHAPE_ID_MAP: dict[int, "TetrominoShape"] = {}

    def __init__(self, name: str, color: str | tuple[int, int, int], shape: list[list[int]] | np.ndarray) -> None:

        self.name = name
        self.color = color
        self.id = len(self.ALL_SHAPES) + 1
        
        TetrominoShape.ALL_SHAPES.append(self)
        TetrominoShape.SHAPE_ID_MAP[self.id] = self

        shape = np.array(shape, dtype=np.uint8)

        self.rotations: list[np.ndarray] = []
        for i in range(TetrominoShape.MAX_ROTATIONS):
            self.rotations.append(shape)
            shape = rotate(shape)
            if np.array_equal(shape, self.rotations[0]):
                break

    def get_name(self) -> str: return self.name

    def get_color(self) -> str | tuple[int, int, int]: return self.color

    def get_id(self) -> int: return self.id

    def get_num_of_rotations(self) -> int: return len(self.rotations)
    
    def get_grid(self, rotation = 0) -> np.ndarray: return self.rotations[rotation]
    
    def get_width(self, rotation = 0) -> int: return self.get_grid(rotation).shape[1]
    
    def get_height(self, rotation = 0) -> int: return self.get_grid(rotation).shape[0]

    def get_trimmed_grid(self, rotation = 0):
        grid = self.get_grid(rotation) 
        
        zeros = np.where(grid != 0)
        grid = grid[min(zeros[0]) : max(zeros[0]) + 1, min(zeros[1]) : max(zeros[1]) + 1]
        
        return grid
        

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.color}, {self.rotations[0]})"


TetrominoShape("I", (0, 240, 240), [
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]),

TetrominoShape("O", (240, 240, 0), [
    [1, 1],
    [1, 1],
]),

TetrominoShape("L", (240, 160, 0), [
    [0, 0, 1],
    [1, 1, 1],
    [0, 0, 0],
]),

TetrominoShape("J", (0, 0, 240), [
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 0],
]),

TetrominoShape("T", (160, 0, 240), [
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0],
]),

TetrominoShape("Z", (240, 0, 0), [
    [1, 1, 0],
    [0, 1, 1],
    [0, 0, 0],
]),

TetrominoShape("S", (0, 240, 0), [
    [0, 1, 1],
    [1, 1, 0],
    [0, 0, 0],
]),


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
