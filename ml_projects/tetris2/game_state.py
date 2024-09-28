import dataclasses

import numpy as np

@dataclasses.dataclass(slots=True)
class State:
    board: np.ndarray

    current_piece_board: np.ndarray
    current_piece_percent_placed: float

    ghost_board: np.ndarray

    held_piece: np.ndarray
    held_piece_usable: bool

    queue: list[np.ndarray]

    info: dict[str, str]
    has_lost: bool

    null_value: int