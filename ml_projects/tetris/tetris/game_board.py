import random
import enum

import numpy as np

from . import shapes
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
        
        self.orientation = orientation % len(self.shape.orientations)
    
    def get_height(self) -> int: return self.get_grid().shape[1]
        
    def get_width(self) -> int: return self.get_grid().shape[0]

    def get_color(self) -> tuple[int, int, int] | str: return self.shape.get_color()
    
    def get_name(self) -> str: return self.shape.get_name()
    
    def get_id(self) -> int: return self.shape.get_id()

    def get_grid(self) -> np.ndarray: return self.shape.get_grid(self.orientation)
     
    def rotate(self) -> None: self.orientation = (self.orientation + 1) % len(self.shape.orientations)
            
    def copy(self) -> "Tetromino": return Tetromino(self.x, self.y, self.shape, self.orientation)

    def __iter__(self):
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                yield (self.get_grid()[row][col], (self.y + row, self.x + col))
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, shape={self.shape}, orientation={self.orientation})"

class Tetris:
    DEFAULT_FPS = 60
    
    MIN_SHAPE_QUEUE_SIZE = 32
    
    def __init__(
        self, width: int, height: int, FPS: int = DEFAULT_FPS,
        enable_wall_kick = True, shape_queue_size: int = None, enable_hold = True) -> None:

        self.width, self.height = width, height
        
        self.fps = FPS
        
        self.visible_shape_queue_size = shape_queue_size
        self.enable_hold = enable_hold
                
        self.shape_bag = [
            shapes.I, shapes.O, shapes.L, shapes.J, shapes.T, shapes.Z
        ]
        
        self.positions_to_try = [(0, 0)]
        if enable_wall_kick:
            self.positions_to_try.extend([(1, 0), (-1, 0)])
        
        self.done: bool
        self.frame: int
        self.score: int
        self.lines: int
        self.lines_cleared_in_last: int
        self.score_in_last: int
        self.level: int
        self.block_drop_interval: int
        
        self.current_tetromino: Tetromino
        
        self.held_shape: TetrominoShape
        self.can_swap: bool
        
        self.shape_queue: list[TetrominoShape]
                
        self.fps_scale = self.fps / self.DEFAULT_FPS
        
        self.reset()
        self._create_inputs_cache()
        self._create_moves_cache()

    def reset(self) -> None:
        self.grid = np.zeros((self.height, self.width), dtype=np.uint8)
        
        self.shape_queue = []
        self.fill_piece_queue()
        
        self.frame = self.score = self.lines = self.lines_cleared_in_last = self.score_in_last = self.level = 0
        self.block_drop_interval = 60 * self.fps_scale
        
        self.done = False

        self.held_shape = None
         
        self.new_figure()
        
    def fill_piece_queue(self):
        while len(self.shape_queue) < self.MIN_SHAPE_QUEUE_SIZE:
            shape_bag_copy = self.shape_bag.copy()
            np.random.shuffle(shape_bag_copy)
            self.shape_queue.extend(shape_bag_copy)

    def get_current_figure(self) -> Tetromino:
        return self.current_tetromino
    
    def new_figure(self) -> None:
        self.can_swap = True
        
        shape = self.shape_queue.pop(0)
        
        self.current_tetromino = Tetromino(
            self.width // 2 - shape.get_width() // 2, 0,
            shape
        )
        
        self.fill_piece_queue()
    
    def get_state(self) -> tuple:
        return (
            self.grid.copy(), self.current_tetromino.copy(), self.shape_queue.copy(), self.held_shape, self.can_swap,
            self.frame, self.score, self.lines, self.lines_cleared_in_last, self.level, self.block_drop_interval, self.done,
        )
    
    def set_state(self, data: tuple) -> None:
        (
            grid, current_tetromino, shape_queue, self.held_shape, self.can_swap,
            self.frame, self.score, self.lines, self.lines_cleared_in_last, self.level, self.block_drop_interval, self.done,
        ) = data
        
        (self.grid, self.current_tetromino, self.shape_queue) = (grid.copy(), current_tetromino.copy(), shape_queue.copy())
                
    def hold(self) -> None:
        if (not self.enable_hold) or (not self.can_swap): return
        
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

    def clear_lines(self, lines: list[int]) -> None:
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
        self.clear_lines(full_line_indexes)

        self.new_figure()

        self.lines_cleared_in_last = len(full_line_indexes)
        
        scores = [0, 40, 100, 300, 1200]
        
        # Optimization
        if self.lines_cleared_in_last > 0:
            self.lines += self.lines_cleared_in_last
            self.score += scores[self.lines_cleared_in_last] * (self.level + 1)
            self.level = (self.lines // 10)

            if self.level < 11: block_drop_interval = 60 - self.level * 5
            elif self.level < 12: block_drop_interval = 9
            elif self.level < 13: block_drop_interval = 8
            elif self.level < 15: block_drop_interval = 7
            elif self.level < 17: block_drop_interval = 6
            elif self.level < 20: block_drop_interval = 5
            elif self.level < 24: block_drop_interval = 4
            elif self.level < 29: block_drop_interval = 3
            elif self.level < 30: block_drop_interval = 3
            else: block_drop_interval = 1
            
            self.block_drop_interval = max(int(block_drop_interval * self.fps_scale), 1)
        
        self.done = self.intersects() 
        
    def change_x(self, dx: int) -> None:
        old_x = self.current_tetromino.x
        self.current_tetromino.x += dx
        if self.intersects():
            self.current_tetromino.x = old_x

    def rotate(self) -> None:
 
        for (dx, dy) in self.positions_to_try:
            self.current_tetromino.x += dx
            self.current_tetromino.y += dy
            
            old_orientation = self.current_tetromino.orientation
            self.current_tetromino.rotate()      
            if self.intersects(): self.current_tetromino.orientation = old_orientation
            else: return
                
            self.current_tetromino.x -= dx
            self.current_tetromino.y -= dy
                
    def step(self, moves: list[Move], quick_return = False) -> tuple[np.ndarray, float, bool, dict]:

        self.frame += 1
        
        self.lines_cleared_in_last = 0
        self.score_in_last = 0
        score_at_start = self.score
        
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
        
        if quick_return:
            return self.state_as_array(), None, None, None
        
        reward = self.value_function()
                
        self.score_in_last = self.score - score_at_start
                
        info = {
            "score": self.score,
            "lines": self.lines,
            "level": self.level,
            "held": self.held_shape,
            "can_hold": self.can_swap,
            "piece_queue": self.shape_queue[:self.visible_shape_queue_size],
            "frame": self.frame,
        }
        
        return self.state_as_array(), reward, self.done, info
        
    def render_as_str(self, block_width = 2, full_block = True) -> str:
        
        full = "[" + " " * (block_width - 2) + "]"
        
        if full_block: full = "█" * block_width

        empty = " " * (block_width - 1) + "."

        line_padding_left = " <!"
        line_padding_right = "!> "

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
            " " * len(line_padding_left)
            + (bottom2 * (self.width * block_width // len(bottom2)))
            + " " * len(line_padding_right)
        )

        return "\n".join(lines)
 
    def __str__(self) -> str:
        return self.render_as_str()
    
    def __iter__(self):
        for row in range(self.height):
            for col in range(self.width):
                yield (self.grid[row][col], (row, col))
    
    # Ai related methods
    
    def _create_moves_cache(self) -> None:
         
        rules = {
            None: 1,
            Move.LEFT: 1,
            Move.RIGHT: 1,
            Move.SPIN: 3,
            Move.HOLD: 1,
            Move.HARD_DROP: 1,
            Move.SOFT_DROP: 1,
        }
         
        self._next_state_moves = [
            tuple([move] * (i + 1))
            for move, repeat in rules.items()
            for i in range(repeat)
        ]
        
    def _create_inputs_cache(self):
        self._one_hot_shapes = np.eye(max(TetrominoShape.SHAPE_ID_MAP.keys()), dtype=np.float64)
        self._one_hot_x = np.eye(self.width, dtype=np.float64)
        self._one_hot_y = np.eye(self.height, dtype=np.float64) 
        self._one_hot_rotations = np.eye(TetrominoShape.MAX_ORIENTATIONS, dtype=np.float64)
        
    def state_as_array(self) -> np.ndarray:
        
        return np.concatenate([
            (self.grid > 0).flatten(), #  board
            
            self._one_hot_shapes[self.current_tetromino.shape.id], # piece type
            self._one_hot_x[self.current_tetromino.x], # x
            self._one_hot_y[self.current_tetromino.y], # y
            self._one_hot_rotations[self.current_tetromino.orientation], # rotation
            
            # np.concatenate([ # next piece types
            #     self._one_hot_shapes[shape]
            #     for shape in self.shape_queue[:self.visible_shape_queue_size]
            # ]), 
            self._one_hot_shapes[self.shape_queue[0].id],  # Next pieces types (optimized)
            self._one_hot_shapes[self.shape_queue[1].id],
            self._one_hot_shapes[self.shape_queue[2].id],
            
            [self.can_swap],
            self._one_hot_shapes[self.held_shape.id if self.held_shape else 0]
        ], dtype=np.float64)
        
    def value_function(self) -> float:                
        heights = self._get_column_heights()
        return self.lines_cleared + (
            -0.510066 * np.sum(heights) 
            -0.536630 * self._get_number_of_holes()
            # -0.084483 * self._heights_bumpiness(heights)
            -0.101044 * np.mean(heights)
             
            +1.2 * self.can_swap
        ) / 25

    
    def get_next_states(self) -> dict[tuple[Move], np.ndarray]:
        output = {}
        
        start_state_array = self.state_as_array()
        
        starting_state = self.get_state()
        
        for moves in self._next_state_moves:               
            state_array, _, _, _ = self.step(moves, quick_return=True)
            if (moves == (None,)) or (not np.array_equal(state_array, start_state_array)): output[moves] = state_array
            
            self.set_state(starting_state)
                    
        return output
    
    def _get_number_of_holes(self) -> int:
        holes = 0

        for col in self.grid.T:
            has_seen_block = False
            for value in col:
                has_seen_block = has_seen_block or value
                holes += (has_seen_block) and not value
        
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