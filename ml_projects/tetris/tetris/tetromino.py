import pygame

MAX_ROTATIONS = 4

class TetrominoBlockShape:
    
    def __init__(self, name: str, color: pygame.Color, shape: list[list[int]]) -> None:
        self.name = name
        self.color = color
        
        self.height = len(shape)
        self.width = len(shape[0])
        
        self.shapes = [shape]
        for i in range(MAX_ROTATIONS):
            shape = TetrominoBlockShape.rotate_clockwise(shape)
            if shape == self.shapes[0]: break
            self.shapes.append(shape)

    @staticmethod
    def rotate_clockwise(matrix: list[list[int]]):
        return list(list(x) for x in zip(*matrix))[::-1]
    
    def __iter__(self) -> tuple[int, int]:
        for row in range(self.height):
            for col in range(self.width):
                yield (row, col)

# https://i.stack.imgur.com/UbPC9.png
SHAPES = [
    TetrominoBlockShape("I", (0, 240, 240), [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
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
        [0, 1, 0],
        [1, 1, 0],
        [1, 0, 0],
    ]),
    TetrominoBlockShape("S", (0,240,0), [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
    ]),
]