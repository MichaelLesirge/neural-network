import random
import enum

import numpy as np

from .shapes import TetrominoShape

class Move(enum.Enum):
    SPIN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()
    SOFT_DROP = enum.auto()
    HARD_DROP = enum.auto()
    HOLD = enum.auto()
    
    QUIT = enum.auto()

class Tetromino:
    WALL_BOUNCING = True
    
    def __init__(self, x: int, y: int, shape: TetrominoShape, orientation: int = 0) -> None:
        self.x = x
        self.y = y
        
        self.shape = shape
        
        self.orientation = orientation % len(self.shape.rotations)
    
    def get_height(self) -> int: return self.get_grid().shape[1]
        
    def get_width(self) -> int: return self.get_grid().shape[0]

    def get_color(self) -> tuple[int, int, int] | str: return self.shape.get_color()
    
    def get_name(self) -> str: return self.shape.get_name()
    
    def get_id(self) -> int: return self.shape.get_id()

    def get_grid(self) -> np.ndarray: return self.shape.get_grid(self.orientation)
     
    def rotate(self) -> None: self.orientation = (self.orientation + 1) % len(self.shape.rotations)            

    def __iter__(self):
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                yield (self.get_grid()[row][col], (self.y + row, self.x + col))

class Tetris:
    DEFAULT_FPS = 60
    
    def __init__(
        self, width: int, height: int, FPS: int = DEFAULT_FPS,
        enable_wall_kick = True, piece_queue_size = False, enable_hold = True) -> None:

        self.width, self.height = width, height
        
        self.fps = FPS
        
        self.enable_wall_kick = enable_wall_kick
        
        if piece_queue_size is False: piece_queue_size = 0
        if piece_queue_size is True: piece_queue_size = 3
        self.piece_queue_size = piece_queue_size
        
        self.enable_hold = enable_hold
        
        self.fps_scale = self.fps / self.DEFAULT_FPS
        
        self.reset()
        self._create_inputs_cache()

    def reset(self) -> None:
        self.grid = np.zeros((self.height, self.width), dtype=np.uint8)
        
        self.shape_queue: list[TetrominoShape] = []
        self.fill_piece_queue()
        
        self.frame = self.score = self.lines = self.level = 0
        self.block_drop_interval = self.DEFAULT_FPS * self.fps_scale
        self.done = False

        self.held_shape: TetrominoShape = None
         
        self.new_figure()
        
    def fill_piece_queue(self):
        while len(self.shape_queue) < self.piece_queue_size:
            shape = random.choice(TetrominoShape.ALL_SHAPES)
            self.shape_queue.append(shape)

    def get_current_figure(self) -> Tetromino:
        return self.current_tetromino

    def new_figure(self) -> None:
        self.can_swap = True
        
        if self.piece_queue_size == 0: shape = random.choice(TetrominoShape.ALL_SHAPES)
        else: shape = self.shape_queue.pop(0)
        
        self.current_tetromino = Tetromino(
            self.width // 2 - shape.get_width() // 2, 0,
            shape
        )
        
        self.fill_piece_queue()
        
    def hold(self) -> None:
        if not (self.enable_hold and self.can_swap): return
        
        starting_current = self.current_tetromino
        if self.held_shape: self.shape_queue.insert(0, self.held_shape)
        
        self.new_figure()
        
        self.can_swap = False
        self.held_shape = starting_current.shape

    def intersects(self) -> bool:
        for value, (row, col) in self.current_tetromino:
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
            self.current_tetromino.y += 1
            
        self.current_tetromino.y -= 1
        self.score -= 2
        
        self.freeze()

    def soft_drop(self):
        self.score += 1
        self.current_tetromino.y += 1
        
        if self.intersects():
            self.current_tetromino.y -= 1
            self.score -= 1
            
    def gravity_drop(self) -> None:
        self.current_tetromino.y += 1
        
        if self.intersects():
            self.current_tetromino.y -= 1
 
            self.freeze()

    def freeze(self) -> bool:
        for value, (row, col) in self.current_tetromino:
            if value: self.grid[row][col] = self.current_tetromino.get_id()
        
        full_line_indexes = self.find_full_lines()
        self.remove_full_lines(full_line_indexes)

        self.new_figure()

        num_of_lines = len(full_line_indexes)
        
        scores = [0, 40, 100, 300, 1200]
        
        # Optimization
        if num_of_lines > 0:
            self.lines += num_of_lines
            self.score += scores[num_of_lines] * (self.level + 1)
            self.level = (self.lines // 10)

            if self.level < 12: block_drop_interval = 60 - self.level*5
            elif self.level < 13: block_drop_interval = 7
            elif self.level < 15: block_drop_interval = 6
            elif self.level < 17: block_drop_interval = 5
            elif self.level < 20: block_drop_interval = 4
            elif self.level < 24: block_drop_interval = 3
            elif self.level < 29: block_drop_interval = 2
            else: block_drop_interval = 1
            
            self.block_drop_interval = max(int(block_drop_interval * self.fps_scale), 1)
        
        self.done = self.intersects() 
        
    def change_x(self, dx: int) -> None:
        old_x = self.current_tetromino.x
        self.current_tetromino.x += dx
        if self.intersects():
            self.current_tetromino.x = old_x

    def rotate(self) -> None:

        positions_to_try = [(0, 0)]
        
        if self.enable_wall_kick:
            positions_to_try.extend([(1, 0), (-1, 0)])
        
        for (dx, dy) in positions_to_try:
            self.current_tetromino.x += dx
            self.current_tetromino.y += dy
            
            old_orientation = self.current_tetromino.orientation
            self.current_tetromino.rotate()      
            if self.intersects(): self.current_tetromino.orientation = old_orientation
            else: return
                
            self.current_tetromino.x -= dx
            self.current_tetromino.y -= dy
                
    def step(self, moves: list[Move]):

        self.frame += 1
        
        soft_drop = False
        for move in moves:
            match move:
                case Move.QUIT: self.done = True
                case Move.SPIN: self.rotate()
                case Move.LEFT: self.change_x(-1)
                case Move.RIGHT: self.change_x(+1)
                case Move.HOLD: self.hold()
                case Move.HARD_DROP: self.hard_drop()
                case Move.SOFT_DROP: soft_drop = True
                case None: pass
         
        is_drop_frame = self.frame % self.block_drop_interval == 0
        is_soft_drop_frame = soft_drop and self.frame % self.fps_scale == 0
            
        if is_drop_frame: self.gravity_drop()
        elif is_soft_drop_frame: self.soft_drop()
        
        reward = self.value_function()
                
        info = {
            "score": self.score,
            "lines": self.lines,
            "level": self.level,
            "held": self.held_shape,
            "piece_queue": self.shape_queue,
            "frame": self.frame,
        }
        
        return self.state(), reward, self.done, info
        
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
                + "".join([full if (tile or (1, (row_index, col_index)) in self.current_tetromino) else empty for col_index, tile in enumerate(row)])
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
 
    def __str__(self) -> str:
        return self.render_as_str()
    
    def __iter__(self):
        for row in range(self.height):
            for col in range(self.width):
                yield (self.grid[row][col], (row, col))
    
    # Ai related methods
    
    def _create_inputs_cache(self):
        self._piece_to_index = dict(((b, a) for (a, b) in enumerate(TetrominoShape.ALL_SHAPES)))
        self._one_hot_shapes = np.eye(len(TetrominoShape.ALL_SHAPES), dtype=np.float64)
        self._one_hot_x = np.eye(self.width, dtype=np.float64)
        self._one_hot_y = np.eye(self.height, dtype=np.float64) 
        self._one_hot_rotations = np.eye(TetrominoShape.MAX_ROTATIONS, dtype=np.float64)
        
    def state(self) -> np.ndarray:
        return np.concatenate([
            (self.grid > 0).flatten(), #  board
            self._one_hot_shapes[self._piece_to_index[self.current_tetromino.shape]], # piece type
            self._one_hot_x[self.current_tetromino.x], # x
            self._one_hot_y[self.current_tetromino.y], # y
            self._one_hot_rotations[self.current_tetromino.orientation], # rotation
        ], dtype=np.float64)
        
    def value_function(self) -> float:
        heights = self._get_column_heights()

        return (
            + (self.height / 2 - np.max(heights)) / self.height
            + (self.height / 2 - np.mean(heights)) / self.height
            - (self._heights_bumpiness(heights) / self.height / self.width)
            - (self._get_number_of_holes()) / self.height
        )

    
    def get_next_states(self) -> dict[Move, np.ndarray]:
        output = {}
        
        is_drop_frame = self.frame % self.block_drop_interval == 0
        # if (is_drop_frame): self.p
        
        output[None] = self.state()
            
        return output
    
    def _get_number_of_holes(self) -> int:
        holes = 0

        for col in self.grid.T:
            has_seen_block = False
            for value in col:
                if (not has_seen_block and value): has_seen_block = True
                holes += (has_seen_block) and value == 0
        
        return holes
    
    def _get_column_heights(self) -> np.ndarray[int] | int:
        mask = self.grid != 0
        return self.height - np.where(mask.any(axis=0), mask.argmax(axis=0), self.height)
    
    def _heights_bumpiness(self, heights: np.ndarray[int]) -> int:
        total_bumpiness = 0
        for i, height in enumerate(heights[:-1]):
            height_difference = height - heights[i + 1]
            total_bumpiness += abs(height_difference)
        return total_bumpiness