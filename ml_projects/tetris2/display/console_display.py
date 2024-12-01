import numpy as np

from game_state import State
from .display import Display
from .colors import Color

class ConsoleDisplay(Display):

    def __init__(self, tetromino_colors: dict[int, Color]) -> None:
        self.tetromino_colors = tetromino_colors

        self.default_color_code = ""
        self.reset_code = "\u001b[0m"
        self.color_code_map = {
            Color.CYAN: "\u001b[36m",
            Color.YELLOW: "\u001b[33m",
            Color.PURPLE: "\u001b[35m",
            Color.GREEN: "\u001b[32m",
            Color.BLUE: "\u001b[34m",
            Color.RED: "\u001b[31m",
            Color.ORANGE: "\u001b[38;5;166m",
        }

        # for n in range(255):
        #     print("\u001b[38;5;" + str(n) + "m")
        #     print("Test", n)
        #     print("\033[0m", end="")

    def update(self, state: State) -> None:

        combined_board = combined_board = np.where(
            state.current_tetromino_board != state.board_null_value,
            state.current_tetromino_board, state.board)

        board = self.get_grid_string(combined_board, state.board_null_value)
        
        lines = 0

        print()
        lines += 1

        print(board)
        lines += 1 + board.count("\n")
        
        print(", ".join(f"{key}: {value}" for key, value in state.info.items()))
        lines += 1

        # print(f"\u001b[{lines}F", end="")
        
    def get_grid_string(
        self, grid: np.ndarray, null_value: int
    ) -> str:

        start_pad = "<!"
        end_pad = "!>"

        full_tile_str = "[]"
        empty_tile_str = " ."

        end_line_1 = "="
        end_line_2 = "\/"

        return "\n".join([
            start_pad + (
                "".join(
                    (
                        self.color_code_map.get(self.tetromino_colors.get(item), self.default_color_code) + full_tile_str + self.reset_code
                        if (item != null_value)
                        else empty_tile_str
                    )
                    for item in row
                )
            ) + end_pad
            for row in grid]
            + [
                start_pad + end_line_1 * (grid.shape[1] * len(full_tile_str) // len(end_line_1)) + end_pad,
                # " " * len(start_pad) + end_line_2 * (grid.shape[1] * len(full_tile_str) // len(end_line_2)) + " " * len(end_pad)
            ]
        )