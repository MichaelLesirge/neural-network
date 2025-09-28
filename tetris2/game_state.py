import dataclasses

import numpy as np

@dataclasses.dataclass(slots=True)
class State:
    board: np.ndarray

    current_tetromino_board: np.ndarray
    current_tetromino_percent_placed: float

    ghost_tetromino_board: np.ndarray

    held_tetromino: np.ndarray
    can_use_held_tetromino: bool

    tetromino_queue: list[np.ndarray]

    info: dict[str, str]
    verbose_info: dict[str, str]

    game_over: bool
    game_paused: bool

    board_null_value: int