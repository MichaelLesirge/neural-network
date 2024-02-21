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
            for col in range(self.get_height()):
                yield (self.image()[row][col], (self.y + row, self.x + col))
            
SCORES = [0, 40, 100, 300, 1200]

class Tetris:
    def __init__(
        self, width: int, height: int,
        drop_delay_frames: int = 1, soft_drop_delay_frames: int = 1,
        enable_wall_kick = True, enable_start_at_top = True) -> None:

        self.width, self.height = width, height
        
        self.enable_wall_kick = enable_wall_kick
        self.enable_start_at_top = enable_start_at_top
        
        self.drop_delay_frames = drop_delay_frames
        self.soft_drop_delay_frames = soft_drop_delay_frames
        
        self.reset()

    def reset(self) -> None:
        self.grid = np.zeros((self.height, self.width), dtype=np.uint8)
        
        self.frame = self.score = self.lines = self.level = 0
        self.done = False
         
        self.new_figure()

    def get_current_figure(self) -> Tetromino:
        return self.current_figure

    def new_figure(self) -> None:
        shape = random.choice(tetromino.ALL_SHAPES)
        
        self.current_figure = Tetromino(
            self.width // 2 - shape.get_largest_dimension() // 2, 0,
            shape,
            rotation=random.randrange(shape.get_num_of_rotations())
        )
        
        if self.enable_start_at_top:
            while not self.intersects(): self.current_figure.y -= 1
            if self.intersects(): self.current_figure.y += 1

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
        
        self.score += SCORES[num_of_lines]
        self.lines += num_of_lines
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
        
        drop_frame = self.frame % self.drop_delay_frames == 0
        soft_drop_frame = soft_drop and self.frame % self.soft_drop_delay_frames == 0
            
        if soft_drop_frame: self.soft_drop()
        elif drop_frame: self.gravity_drop()
          
        reward = 0
        
        info = {
            "score": self.score,
            "lines": self.lines,
            "lines": self.level,
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

    def render_as_pygame(self, block_size: int = 25, background_color: pygame.Color = "black", line_color: pygame.Color = "white", outline_color: pygame.Color = "white", *, block_images = True, ghost_block = True, blank_surface = False) -> pygame.Surface:
                
        screen = pygame.Surface((self.width * block_size, self.height * block_size))
        
        if blank_surface: return screen
        
        def draw_box(row: int, col: int, color = "white", width = 0, border_radius = -1, margin = 0):
            pygame.draw.rect(screen, color, pygame.Rect(
                col * block_size + margin, row * block_size + margin,
                block_size - margin, block_size - margin
            ), width = width, border_radius = border_radius)            
                        
        def draw_tetromino_block(row: int, col: int, shape: tetromino.TetrominoBlockShape, ghost = False):
            if block_images:
                image = shape.image_ghost if ghost else shape.image
                if image.get_width() != block_size: image = pygame.transform.scale(image, (block_size, block_size))
                screen.blit(image, pygame.Rect(col * block_size, row * block_size, block_size, block_size))
            else:
                print(shape.get_color())
                draw_box(row, col, color=shape.get_color(), margin=1, border_radius=2, width = ghost)

        screen.fill(background_color)
        
        # for col in range(self.width + 1):
        #     pygame.draw.line(screen, line_color, (game_x + block_size * col, game_y), (game_x + block_size * col, game_y + block_size * self.height), width=1)

        # for row in range(self.height + 1):
        #     pygame.draw.line(screen, line_color, (game_x, game_y + block_size * row), (game_x + block_size * self.width, game_y + block_size * row), width=1)

        for value, (row, col) in self:
            if value: draw_tetromino_block(row, col, tetromino.SHAPE_ID_MAP[value])
            draw_box(row, col, color=line_color, width = 1, border_radius=2)
                
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
        
        if outline_color: pygame.draw.rect(screen, outline_color, pygame.Rect(
            0, 0, block_size * self.width, block_size * self.height 
        ), width=1)
        
        return screen
        
    def __iter__(self):
        for row in range(self.height):
            for col in range(self.width):
                yield (self.grid[row][col], (row, col))