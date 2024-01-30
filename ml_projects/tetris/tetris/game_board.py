import random

from . import tetromino

class Tetromino:
    def __init__(self, x: int, y: int, type: tetromino.TetrominoBlockShape, rotation: int = 0) -> None:
        self.x = x
        self.y = y
        
        self.width, self.height = type.width, type.height

        self.type = type
        
        self.rotation = rotation % len(self.type.shapes)
        
    def get_y(self) -> int:
        return int(self.y)

    def get_x(self) -> int:
        return int(self.x)

    def get_color(self) -> [tuple[int, int, int] | str]:
        return self.type.color
    
    def get_name(self) -> str:
        return self.type.name

    def image(self) -> list[list[int]]:
        return self.type.shapes[self.rotation]
    
    def rotate(self) -> None:
        self.rotation = (self.rotation + 1) % len(self.type.shapes)
        self.width, self.height = self.height, self.width

    def __iter__(self) -> tuple[int, tuple[int, int]]:
        for row in range(self.height):
            for col in range(self.width):
                yield (self.image()[row][col], (row, col))
            

class GameBoard:
    def __init__(self, width: int, height: int) -> None:

        self.width, self.height = width, height

        self.grid = [[None] * self.width for i in range(self.height)]
        
        self.score = 0
        self.done = False
        
        self.new_figure()

    def get_current_figure(self) -> None:
        return self.current_figure

    def new_figure(self) -> None:
        self.current_figure = Tetromino(self.width // 2, 0, random.choice(tetromino.SHAPES), rotation=random.randrange(tetromino.MAX_ROTATIONS))

    def intersects(self) -> bool:
        for row, col in self.current_figure.type:
            if self.current_figure.image()[row][col] and ( 
                row + self.current_figure.y >= self.height or
                col + self.current_figure.x >= self.width or
                col + self.current_figure.x < 0 or
                self.grid[row + self.current_figure.y][col + self.current_figure.x] is not None
            ):
                return True
        return False
        
    def find_full_lines(self) -> list[int]:
        lines = []
        
        for i, row in enumerate(self.grid):
            if all(row): lines.append(i)
                        
        return lines

    def remove_full_lines(self, lines: list[int]) -> None:
        for line in sorted(lines, reverse=True): self.grid.pop(line)
        for line in lines: self.grid.insert(0, [None] * self.width)
    
    def hard_drop(self) -> None:
        while not self.intersects():
            self.current_figure.y += 1
        self.current_figure.y -= 1
        self.freeze()

    def soft_drop(self) -> None:
        self.current_figure.y += 1
        if self.intersects():
            self.current_figure.y -= 1
            self.freeze()

    def freeze(self) -> bool:
        for value, (row, col) in self.current_figure:
            if value: self.grid[row + self.current_figure.y][col + self.current_figure.x] = self.current_figure.get_color()

        lines = self.find_full_lines()
        self.remove_full_lines(lines)

        self.new_figure()

        self.score += len(lines) ** 2
        self.done = self.intersects() 
        
    def change_x(self, dx: int) -> None:
        old_x = self.current_figure.x
        self.current_figure.x += dx
        if self.intersects():
            self.current_figure.x = old_x

    def rotate(self) -> None:
        old_rotation = self.current_figure.rotation
        self.current_figure.rotate()
        if self.intersects():
            self.current_figure.rotation = old_rotation
    
    def __iter__(self) -> tuple[str | tuple[int, int, int] | None, tuple[int, int]]:
        for row in range(self.height):
            for col in range(self.width):
                yield (self.grid[row][col], (row, col))