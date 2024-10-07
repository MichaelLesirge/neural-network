import numpy as np

class Model:

    def reset(self) -> None:
        pass
    
    def step(self) -> None:
        pass
        
    def rotate(self, rotations: int) -> None:
        pass
        
    def change_x(self, dx: int) -> None:
        pass
    
    def get_board(self) -> np.ndarray:
        return None

    def get_current_piece_board(self) -> np.ndarray:
        return None

    def get_piece_percent_placed(self) -> float:
        return 0

    def get_ghost_board(self) -> np.ndarray:
        return None

    def get_held_tetromino(self) -> np.ndarray | None:
        return None

    def can_use_held_tetromino(self) -> bool:
        return False

    def get_tetromino_queue(self) -> list[np.ndarray]:
        return []

    def get_array_null_value(self) -> int:
        return None
    