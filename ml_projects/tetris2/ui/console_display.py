import numpy as np

from .display import Display

class ConsoleDisplay(Display):

    def __init__(self, row_template_str="[%s]", full_tile_template_str=" %s", empty_tile_str="  ") -> None:
        self.row_template_str = row_template_str
        self.full_tile_template_str = full_tile_template_str
        self.empty_tile_str = empty_tile_str
    
    def update(self, presenter) -> None:
        print(", ".join(f"{key}: {value}" for key, value in state.info.items()))

        combined_board = combined_board = np.where(
            state.current_tetromino_board != state.board_null_value,
            state.current_tetromino_board, state.board)

        print(self.get_grid_string(combined_board, state.board_null_value))
        
    def get_grid_string(
        self, grid: np.ndarray, null_value: int
    ) -> str:

        return "\n".join(
            self.row_template_str
            % (
                "".join(
                    (
                        self.full_tile_template_str % item
                        if (item != null_value)
                        else self.empty_tile_str
                    )
                    for item in row
                )
            )
            for row in grid
        )