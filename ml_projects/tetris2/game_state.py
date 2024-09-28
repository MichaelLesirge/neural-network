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
    has_lost: bool

    board_null_value: int