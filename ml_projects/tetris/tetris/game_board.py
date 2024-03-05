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
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, shape={self.shape}, orientation={self.orientation})"

class Tetris:
    DEFAULT_FPS = 60
    
    def __init__(
        self, width: int, height: int, FPS: int = DEFAULT_FPS,
        enable_wall_kick = True, shape_queue_size: int = None, enable_hold = True) -> None:

        self.width, self.height = width, height
        
        self.fps = FPS
        
        self.enable_wall_kick = enable_wall_kick
        
        if shape_queue_size is None: shape_queue_size = 0
        self.shape_queue_size = shape_queue_size
        
        self.done: bool
        self.frame: int
        self.score: int
        self.lines: int
        self.level: int
        
        self.block_drop_interval: int
        
        self.current_tetromino: Tetromino
        
        self.held_shape: TetrominoShape
        self.can_swap: bool
        
        self._shape_queue: list[TetrominoShape]
        
        self.enable_hold = enable_hold
        
        self.fps_scale = self.fps / self.DEFAULT_FPS
        
        self.reset()
        self._create_inputs_cache()

    def reset(self) -> None:
        self.grid = np.zeros((self.height, self.width), dtype=np.uint8)
        
        self._shape_queue = []
        self.fill_piece_queue()
        
        self.frame = self.score = self.lines = self.level = 0
        self.block_drop_interval = self.DEFAULT_FPS * self.fps_scale
        
        self.done = False

        self.held_shape = None
         
        self.new_figure()
        
    def fill_piece_queue(self):
        while len(self._shape_queue) < self.shape_queue_size + 1:
            shape = random.choice(TetrominoShape.ALL_SHAPES)
            self._shape_queue.append(shape)

    def get_current_figure(self) -> Tetromino:
        return self.current_tetromino
    
    @property
    def shape_queue(self):
        return self._shape_queue[:-1]

    def new_figure(self) -> None:
        self.can_swap = True
        
        shape = self._shape_queue.pop(0)
        
        self.current_tetromino = Tetromino(
            self.width // 2 - shape.get_width() // 2, 0,
            shape
        )
        
        self.fill_piece_queue()
    
    def get_state(self) -> tuple:
        return (
            self.grid.copy(), self._shape_queue.copy(), self.held_shape, self.can_swap,
            self.current_tetromino, (self.current_tetromino.x, self.current_tetromino.y, self.current_tetromino.orientation),
            self.frame, self.score, self.lines, self.level, self.block_drop_interval, self.done,
        )
    
    def set_state(self, data: tuple) -> None:
        (
            self.grid, self._shape_queue, self.held_shape, self.can_swap,
            self.current_tetromino, (self.current_tetromino.x, self.current_tetromino.y, self.current_tetromino.orientation),
            self.frame, self.score, self.lines, self.level, self.block_drop_interval, self.done,
        ) = data
                
    def hold(self) -> None:
        if not (self.enable_hold and self.can_swap): return
        
        starting_current = self.current_tetromino
        if self.held_shape: self._shape_queue.insert(0, self.held_shape)
        
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
                
    def step(self, moves: list[Move], quick_return = False) -> tuple[np.ndarray, float, bool, dict]:

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
        
        if quick_return:
            return self.state_as_array(), None, None, None
        
        reward = self.value_function()
                
        info = {
            "score": self.score,
            "lines": self.lines,
            "level": self.level,
            "held": self.held_shape,
            "piece_queue": self.shape_queue,
            "frame": self.frame,
        }
        
        return self.state_as_array(), reward, self.done, info
        
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
        
    def state_as_array(self) -> np.ndarray:
        
        state = self.get_state()
        self.hard_drop()
        hard_drop_grid = (self.grid > 0).flatten()
        self.set_state(state)
        
        return np.concatenate([
            (self.grid > 0).flatten(), #  board
            hard_drop_grid, # board after hard drop (ghost block like feature)
            self._one_hot_shapes[self._piece_to_index[self.current_tetromino.shape]], # piece type
            self._one_hot_x[self.current_tetromino.x], # x
            self._one_hot_y[self.current_tetromino.y], # y
            self._one_hot_rotations[self.current_tetromino.orientation], # rotation
            self._one_hot_shapes[self._piece_to_index[self._shape_queue[0]]], # next piece type
        ], dtype=np.float64)
        
    def value_function(self) -> float:        
        heights = self._get_column_heights()
        return 1 - (
            + 0.5 * (self._get_number_of_holes() / self.width)
            + 0.3 * (np.max(heights) / self.height)
            + 0.2 * (np.mean(heights) / self.height)
            + 0.1 * (self._heights_bumpiness(heights) / self.height)
        ) * 2 - (5 * self.done)

    
    _next_state_move = [None, Move.LEFT, Move.RIGHT, Move.SPIN]
    def get_next_states(self) -> dict[Move, np.ndarray]:
        output = {}
        
        start_state_array = self.state_as_array()
        
        for move in self._next_state_move:
            state = self.get_state()
            state_array, _, _, _ = self.step([move], quick_return=True)
            if (move is None) or not np.array_equal(state_array, start_state_array): output[move] = state_array
            self.set_state(state)
        
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