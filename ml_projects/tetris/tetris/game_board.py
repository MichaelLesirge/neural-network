import random
import enum

import numpy as np
import pygame

from . import tetromino

class Move(enum.Enum):
    SPIN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()
    SOFT_DROP = enum.auto()
    HARD_DROP = enum.auto()
    
    QUIT = enum.auto()
    
class Render(enum.Enum):
    ANSI = enum.auto()
    PYGAME = enum.auto

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

    def get_color(self) -> tuple[int, int, int] | str:
        return self.type.color
    
    def get_name(self) -> str:
        return self.type.name
    
    def get_id(self) -> int:
        return self.type.id

    def image(self) -> np.ndarray:
        return self.type.shapes[self.rotation]
     
    def rotate(self) -> None:
        self.rotation = (self.rotation + 1) % len(self.type.shapes)
        self.width, self.height = self.height, self.width

    def __iter__(self):
        for row, col in self.type:
            yield (self.image()[row][col], (self.y + row, self.x + col))
            
SCORES = [0, 40, 100, 300, 1200]

class Tetris:
    def __init__(self, width: int, height: int, drop_every = 1) -> None:

        self.width, self.height = width, height
        self.drop_every = drop_every
        
        self.reset()

    def reset(self) -> None:
        self.grid = np.zeros((self.height, self.width), dtype=np.uint8)
        
        self.score = 0
        self.done = False
        
        self.frame = 0
        
        self.new_figure()

    def get_current_figure(self) -> tetromino.TetrominoBlockShape:
        return self.current_figure

    def new_figure(self) -> None:
        self.current_figure = Tetromino(self.width // 2, 0, random.choice(tetromino.SHAPES), rotation=random.randrange(tetromino.MAX_ROTATIONS))

    def intersects(self) -> bool:
        for value, (row, col) in self.current_figure:
            if value and ( 
                row >= self.height or col >= self.width or col < 0 or
                self.grid[row][col] != 0
            ):
                return True
        return False
        
    def find_full_lines(self) -> list[int]:
        return [i for i, row in enumerate(self.grid) if all(row)]

    def remove_full_lines(self, lines: list[int]) -> None:
        for line in lines:
            self.grid[1:line + 1, :] = self.grid[:line, :]
            self.grid[0, :] = 0
    
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
            if value: self.grid[row][col] = self.current_figure.get_id()

        lines = self.find_full_lines()
        self.remove_full_lines(lines)

        self.new_figure()

        # self.score += (len(lines) ** 2) * 100
        self.score += SCORES[len(lines)]
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
            
    def step(self, moves: Move | list[Move]):
        
        if isinstance(moves, Move):
            moves = [moves]
        
        soft_drop = False
        for move in moves:
            match move:
                case Move.QUIT: self.done = True
                case Move.SPIN: self.rotate()
                case Move.LEFT: self.change_x(-1)
                case Move.RIGHT: self.change_x(+1)
                case Move.HARD_DROP: self.hard_drop()
                case Move.SOFT_DROP: soft_drop = True
        
        drop_frame = self.frame % self.drop_every == 0
        if drop_frame or soft_drop:
            self.soft_drop()
        
        self.frame += 1
        
        reward = 0
        
        info = {
            "score": self.score,
            "frame": self.frame,
            "drop_frame": drop_frame
        }
        
        return self.grid, reward, self.done, info
    
    def render(self, mode: Render = Render.ANSI, *args, **kwargs) -> str:
        match mode:
            case Render.ANSI:
                return self.render_as_str(*args, **kwargs)
            case Render.PYGAME:
                return self.render_as_pygame(*args, **kwargs)
        
    def render_as_str(self, block_width = 2) -> str:
        full = "[" + " " * (block_width - 2) + "]"

        empty = " " * (block_width - 1) + "."

        line_padding_left = "〈!"
        line_padding_right = "!〉"
        line_padding_width = 3  # Angle brackets have space built in

        lines = []

        for row_index, row in enumerate(self.grid):
            lines.append(
                line_padding_left
                + "".join([full if (tile or (1, (row_index, col_index)) in self.current_figure) else empty for col_index, tile in enumerate(row)])
                + line_padding_right
            )

        bottom1 = "="
        lines.append(
            line_padding_left + bottom1 * (self.width * block_width // len(bottom1)) + line_padding_right
        )

        bottom2 = "\\/"
        lines.append(
            " " * line_padding_width
            + (bottom2 * (self.width * block_width // len(bottom2)))
            + " " * line_padding_width
        )

        return "\n".join(lines)

    def render_a_pygame(self, screen: pygame.Surface, block_size: int = 20, top_left_coordinate: tuple[int, int] = (0, 0), background_color: pygame.Color = "black", line_color: pygame.color = "white", main_color: pygame.color = "white"):
        
        game_x, game_y = top_left_coordinate
        
        def draw_box(row: int, col: int, color = "white", width = 0, border_radius = -1, margin = 0):
            pygame.draw.rect(screen, color, pygame.Rect(
                game_x + col * block_size + margin, game_y + row * block_size + margin,
                block_size - margin, block_size - margin
            ), width = width, border_radius = border_radius)            

        screen.fill(background_color)
        
        for col in range(self.width + 1):
            pygame.draw.line(screen, line_color, (game_x + block_size * col, game_y), (game_x + block_size * col, game_y + block_size * self.height), width=1)

        for row in range(self.height + 1):
            pygame.draw.line(screen, line_color, (game_x, game_y + block_size * row), (game_x + block_size * self.width, game_y + block_size * row), width=1)

        for value, (row, col) in self:
            if value: draw_box(row, col, color=tetromino.COLOR_MAP[value], margin=1, border_radius=2)
            draw_box(row, col, color=line_color, width = 1)
                
        for value, (row, col) in self.current_figure:
            if value: draw_box(row, col, color=self.current_figure.get_color(), margin=1, border_radius=2)

        
        pygame.draw.rect(screen, main_color, pygame.Rect(
            game_x, game_y, block_size * self.width, block_size * self.height 
        ), width=1)
        
    def __iter__(self):
        for row in range(self.height):
            for col in range(self.width):
                yield (self.grid[row][col], (row, col))