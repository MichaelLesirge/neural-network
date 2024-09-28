import numpy as np

from game_state import State
from .display import Display

class ConsoleDisplay(Display):
    def update(self, state: State) -> None:
        print(", ".join(f"{key}: {value}" for key, value in state.info.items()))

        combined_board = combined_board = np.where(
            state.current_piece_board != state.null_value,
            state.current_piece_board, state.board)

        print(self.get_grid_string(combined_board, state.null_value))
        
    def get_grid_string(
        self, grid: np.ndarray, null_value: int, row_template_str="[%s]", full_tile_template_str=" %s", empty_tile_str="  "
    ) -> str:

        return "\n".join(
            row_template_str
            % (
                "".join(
                    (
                        full_tile_template_str % item
                        if (item != null_value)
                        else empty_tile_str
                    )
                    for item in row
                )
            )
            for row in grid
        )