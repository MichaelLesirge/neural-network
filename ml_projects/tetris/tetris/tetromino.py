import numpy as np

MAX_ROTATIONS = 4

def drop(matrix: list[list[int]]) -> list[list[int]]:
    i = 0
    for row in reversed(matrix):
        if any(row): break
        i += 1
    return np.roll(matrix, i, 0)

COLOR_MAP = {}
class TetrominoBlockShape:
    
    def __init__(self, name: str, color: tuple[int, int, int] | str, shape: list[list[int]], rotators: list = None) -> None:
        self.name = name
        self.color = color
        
        self.id = ord("a") - ord(self.name) + 1
        
        COLOR_MAP[self.id] = color
        
        shape: np.ndarray = np.array(shape, dtype=np.uint8)
        self.height, self.width = shape.shape
        
        if rotators is None: rotators = [np.rot90]
        
        self.shapes = []
        for i in range(MAX_ROTATIONS):
            self.shapes.append(shape)
            for rotator in rotators: shape = rotator(shape)
            if np.array_equal(shape, self.shapes[0]): break
    
    def __iter__(self):
        for row in range(self.height):
            for col in range(self.width):
                yield (row, col) 
  
# https://i.stack.imgur.com/UbPC9.png
SHAPES = [
    TetrominoBlockShape("I", (0, 240, 240), [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]),
    TetrominoBlockShape("O", (240,240,0), [
        [1, 1],
        [1, 1],
    ]),
    TetrominoBlockShape("L", (240,160,0), [
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]),
    TetrominoBlockShape("J", (0,0,240), [
        [0, 1, 1],
        [0, 1, 0],
        [0, 1, 0],
    ]),
    TetrominoBlockShape("T", (160,0,240), [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]),
    TetrominoBlockShape("Z", (240,0,0), [
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 1],
    ]),
    TetrominoBlockShape("S", (0,240,0), [
        [0, 0, 0],
        [0, 1, 1],
        [1, 1, 0],
    ]),
]

def main() -> None:
    states = [" .", "██"]
    
    for shape in SHAPES:
        print(shape.name + ": ")
        for i, orientations in enumerate(shape.shapes):
            print()
            print("\n".join(
                "".join(states[value] for value in row) for row in orientations
            ))
        print()

if __name__ == "__main__":
    main()