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
    WALL_BOUNCING = True
    
    def __init__(self, x: int, y: int, type: tetromino.TetrominoBlockShape, rotation: int = 0) -> None:
        self.x = x
        self.y = y
        
        self.type = type
        
        self.rotation = rotation % len(self.type.rotations)
    
    def get_height(self) -> int: return self.image().shape[1]
        
    def get_width(self) -> int: return self.image().shape[0]

    def get_color(self) -> tuple[int, int, int] | str: return self.type.get_color()
    
    def get_name(self) -> str: return self.type.get_name()
    
    def get_id(self) -> int: return self.type.get_id()

    def image(self) -> np.ndarray: return self.type.rotations[self.rotation]
     
    def rotate(self) -> None: self.rotation = (self.rotation + 1) % len(self.type.rotations)            

    def __iter__(self):
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                yield (self.image()[row][col], (self.y + row, self.x + col))

class Tetris:
    DEFAULT_FPS = 60
    
    def __init__(
        self, width: int, height: int, FPS: int = 1,
        enable_wall_kick = True, piece_queue_size = None) -> None:

        self.width, self.height = width, height
        
        self.fps = FPS
        
        self.enable_wall_kick = enable_wall_kick
        
        if piece_queue_size is None: piece_queue_size = 0
        self.piece_queue_size = piece_queue_size
        
        self.reset()

    def reset(self) -> None:
        self.grid = np.zeros((self.height, self.width), dtype=np.uint8)
        
        self.piece_queue: list[tetromino.TetrominoBlockShape] = []
        self.fill_piece_queue()
        
        self.frame = self.score = self.lines = self.level = 0
        self.done = False
         
        self.new_figure()
        
    def fill_piece_queue(self):
        while len(self.piece_queue) < self.piece_queue_size:
            shape = random.choice(tetromino.ALL_SHAPES)
            self.piece_queue.append(shape)

    def get_current_figure(self) -> Tetromino:
        return self.current_figure

    def new_figure(self) -> None:
        if self.piece_queue_size == 0: shape = random.choice(tetromino.ALL_SHAPES)
        else: shape = self.piece_queue.pop(0)
        
        self.current_figure = Tetromino(
            self.width // 2 - shape.get_width() // 2, 0,
            shape
        )
        
        self.fill_piece_queue()

    def intersects(self) -> bool:
        for value, (row, col) in self.current_figure:
            if value and ( 
                row >= self.height or row < 0 or col >= self.width or col < 0 or
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
            self.score += 2
            self.current_figure.y += 1
            
        self.current_figure.y -= 1
        self.score -= 2
        
        self.freeze()

    def soft_drop(self):
        self.score += 1
        self.current_figure.y += 1
        
        if self.intersects():
            self.current_figure.y -= 1
            self.score -= 1
            
            self.freeze()

    def gravity_drop(self) -> None:
        self.current_figure.y += 1
        
        if self.intersects():
            self.current_figure.y -= 1
 
            self.freeze()

    def freeze(self) -> bool:
        for value, (row, col) in self.current_figure:
            if value: self.grid[row][col] = self.current_figure.get_id()
        
        full_line_indexes = self.find_full_lines()
        self.remove_full_lines(full_line_indexes)

        self.new_figure()

        num_of_lines = len(full_line_indexes)
        
        scores = [0, 40, 100, 300, 1200]
        
        self.score += scores[num_of_lines] * (self.level + 1)
        self.lines += num_of_lines
        self.level = (num_of_lines // 10)
        
        self.done = self.intersects() 
        
    def change_x(self, dx: int) -> None:
        old_x = self.current_figure.x
        self.current_figure.x += dx
        if self.intersects():
            self.current_figure.x = old_x

    def rotate(self) -> None:

        positions_to_try = [(0, 0)]
        
        if self.enable_wall_kick:
            positions_to_try.extend([(1, 0), (-1, 0)])
        
        for (dx, dy) in positions_to_try:
            self.current_figure.x += dx
            self.current_figure.y += dy
            
            old_rotation = self.current_figure.rotation
            self.current_figure.rotate()      
            if self.intersects(): self.current_figure.rotation = old_rotation
            else: return
                
            self.current_figure.x -= dx
            self.current_figure.y -= dy
            
    def step(self, moves: Move | list[Move]):

        self.frame += 1
        
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
        
        if self.level < 12: block_drop_interval = 60 - self.level*5
        elif self.level < 13: block_drop_interval = 7
        elif self.level < 15: block_drop_interval = 6
        elif self.level < 17: block_drop_interval = 5
        elif self.level < 20: block_drop_interval = 4
        elif self.level < 24: block_drop_interval = 3
        elif self.level < 29: block_drop_interval = 2
        else: block_drop_interval = 1
        
        fps_scale = self.fps / self.DEFAULT_FPS
        
        block_drop_interval *= fps_scale
        
        is_drop_frame = self.frame % max(int(block_drop_interval), 1) == 0
        is_soft_drop_frame = soft_drop and self.frame % fps_scale == 0
            
        if is_soft_drop_frame: self.soft_drop()
        elif is_drop_frame: self.gravity_drop()
          
        reward = 0
        
        info = {
            "score": self.score,
            "lines": self.lines,
            "level": self.level,
            "piece_queue": self.piece_queue,
            "frame": self.frame,
        }
        
        return self.grid, reward, self.done, info
    
    def render(self, mode: Render = Render.ANSI, *args, **kwargs) -> str:
        match mode:
            case Render.ANSI:
                return self.render_as_str(*args, **kwargs)
            case Render.PYGAME:
                return self.render_as_pygame(*args, **kwargs)
        
    def render_as_str(self, block_width = 2, full_block = True) -> str:
        
        full = "[" + " " * (block_width - 2) + "]"
        
        if full_block: full = "█" * block_width

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

    def render_as_pygame(self, block_size: int = 25, background_color: pygame.Color = "black", line_color: pygame.Color = "white", *, ghost_block = True) -> tuple[pygame.Surface, list[pygame.Surface]]:
        screen = pygame.Surface((self.width * block_size, self.height * block_size))

        def draw_tetromino_block(row: int, col: int, shape: tetromino.TetrominoBlockShape, ghost = False):
            image = shape.image_ghost if ghost else shape.image
            if image.get_width() != block_size: image = pygame.transform.scale(image, (block_size, block_size))
            screen.blit(image, pygame.Rect(col * block_size, row * block_size, block_size, block_size))
                            
        screen.fill(background_color)
        
        for col in range(1, self.width):
            pygame.draw.line(screen, line_color, (block_size * col, 0), (block_size * col, block_size * self.height), width=1)

        for row in range(1, self.height):
            pygame.draw.line(screen, line_color, (0, block_size * row), (block_size * self.width, block_size * row), width=1)

        for value, (row, col) in self:
            if value: draw_tetromino_block(row, col, tetromino.SHAPE_ID_MAP[value])
                
        for value, (row, col) in self.current_figure:
            if value: draw_tetromino_block(row, col, self.current_figure.type)
         
        if ghost_block:   
            real_y = self.current_figure.y
            
            while not self.intersects():
                self.current_figure.y += 1
            self.current_figure.y -= 1
        
            for value, (row, col) in self.current_figure:
                if value: draw_tetromino_block(row, col, self.current_figure.type, ghost=True)
            
            self.current_figure.y = real_y
        
        return screen
        
    def __iter__(self):
        for row in range(self.height):
            for col in range(self.width):
                yield (self.grid[row][col], (row, col))