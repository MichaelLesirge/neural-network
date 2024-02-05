MAX_ROTATIONS = 4

class TetrominoBlockShape:
    
    def __init__(self, name: str, color: tuple[int, int, int] | str, shape: list[list[int]], rotators: list = None) -> None:
        self.name = name
        self.color = color
        
        self.height = len(shape)
        self.width = len(shape[0])
        
        if rotators is None: rotators = [TetrominoBlockShape.rotate_counterclockwise]
        
        self.shapes = []
        for i in range(MAX_ROTATIONS):
            self.shapes.append(shape)
            for rotator in rotators: shape = rotator(shape)
            if shape == self.shapes[0]: break

    @staticmethod
    def rotate_clockwise(matrix: list[list[int]]) -> list[list[int]]:
        return list(list(x) for x in zip(*matrix))[::-1]

    @staticmethod
    def rotate_counterclockwise(matrix: list[list[int]]) -> list[list[int]]:
        return list(list(x)[::-1] for x in zip(*matrix))

    @staticmethod
    def drop(matrix: list[list[int]]) -> list[list[int]]:
        i = 0
        for row in reversed(matrix):
            if any(row): break
            i += 1
        return matrix[-i:] + matrix[:-i]
    
    def __iter__(self) -> tuple[int, int]:
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
    ], [TetrominoBlockShape.rotate_clockwise, TetrominoBlockShape.drop]),
    TetrominoBlockShape("S", (0,240,0), [
        [0, 0, 0],
        [0, 1, 1],
        [1, 1, 0],
    ], [TetrominoBlockShape.rotate_clockwise, TetrominoBlockShape.drop]),
]

def main() -> None:
    states = [" .", "██"]
    
    for shape in SHAPES:
        print(shape.name + ": ")
        for i, orientations in enumerate(shape.shapes):
            print(i + 1)
            print("\n".join(
                "".join(states[value] for value in row) for row in orientations
            ))
        print()

if __name__ == "__main__":
    main()