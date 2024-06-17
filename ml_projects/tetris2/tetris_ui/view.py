import pygame
import numpy as np

from grid import GridContext, Align
from tetromino import TetrominoTiles

xyPair = tuple[int, int] | pygame.Vector2
ColorValue = tuple[int, int, int] | str


class TetrisRenderer:
    def __init__(
        self,
        tetrominos: TetrominoTiles,
        ghost_tetrominos: TetrominoTiles,
        color: ColorValue = (255, 255, 255),
        background_color: ColorValue = (0, 0, 0),
        secondary_color: ColorValue = (50, 50, 50),
        outline_width=3,
    ) -> None:
        self.tetrominos = tetrominos
        self.ghost_tetrominos = ghost_tetrominos

        self.color = color
        self.secondary_color = secondary_color
        self.background_color = background_color
        self.outline_width = outline_width

    def draw_board(
        self,
        grid: GridContext,
        board: np.ndarray,
        show_grid=False,
    ) -> None:

        sqaure_size = grid.to_pixel_relative((1, 1))

        squares = self.tetrominos.get_tetroino_tiles(board)

        filler_square = pygame.Surface(sqaure_size, pygame.SRCALPHA)
        pygame.draw.rect(
            filler_square,
            self.secondary_color,
            pygame.Rect((0, 0), filler_square.get_size()),
            width=1,
        )

        for y, row in enumerate(squares):
            for x, square in enumerate(row):
                if show_grid:
                    grid.blit(filler_square, (x, y))
                if square:
                    grid.blit(
                        square,
                        (x, y),
                    )

        grid.outline(self.outline_width, self.color)

    def create_item_piece(self, grid_size: int, board: np.ndarray, min_size: xyPair) -> pygame.Surface:

        min_size = pygame.Vector2(min_size) * grid_size

        zeros = np.where(board != 0)
        board = board[min(zeros[0]) : max(zeros[0]) + 1, min(zeros[1]) : max(zeros[1]) + 1]

        board_size = pygame.Vector2(board.T.shape) * grid_size

        board_surface = pygame.Surface(board_size * grid_size)
        self.draw_board(GridContext(board_surface, grid_size), board, show_grid=False)

        size = pygame.Vector2(max(board_size.x, min_size.x), max(board_size.y, min_size.y))
        surface = pygame.Surface(size)

        surface.blit(board_surface, (size - board_size) / 2)

        return surface

    def create_item_text(
        self, size: xyPair, text: str, color: ColorValue, background: ColorValue
    ) -> pygame.Surface:

        surface = pygame.Surface(size)

        if background:
            surface.fill(background)

        font = pygame.font.SysFont("Berlin Sans FB", int(size.y), False, False)
        text_surface = font.render(text, True, color)

        surface.blit(text_surface, (size - text_surface.get_size()) / 2)

        return surface

    def draw_items_box(
        self, grid: GridContext, info: dict[str, list[pygame.Surface]]
    ) -> None:
        grid.fill(self.secondary_color)
        grid.outline(self.outline_width, self.color)

        title_height = 1
        gap_height = 1

        width = grid.get_grid_size().x
        height = 0

        height += gap_height
        for title, data in info.items():

            grid.blit(
                self.create_item_text(
                    grid.to_pixel_relative((width, title_height)),
                    title.upper(),
                    self.color,
                    self.secondary_color,
                ),
                (width / 2, height),
                alignX=Align.CENTER,
            )
            height += title_height

            for data_item in data:
                grid.blit(data_item, (width / 2, height), alignX=Align.CENTER)
                height += data_item.get_height() / grid.get_square_pixels()

            height += gap_height

    def draw_title(self, grid: GridContext, title: str, font_size: int):
        title_font = pygame.font.SysFont("Monospace", font_size, True, False)
        title_surface = title_font.render(title, True, self.color)
        grid.blit(title_surface, (grid.get_grid_size().x / 2, 0), alignX=Align.CENTER)

    def draw_tetris(
        self,
        grid: GridContext,
        board: np.ndarray,
        info: dict[str, str],
        queue: list[np.ndarray],
        held_piece: np.ndarray,
    ) -> pygame.Surface:
        grid.fill(self.background_color)

        # --- Center ---

        # Board
        board_size = pygame.Vector2(board.T.shape)
        board_location = (grid.get_grid_size() - board_size) / 2
        self.draw_board(
            grid.with_focused_window(board_location, board_size),
            board,
            show_grid=True,
        )

        # Title
        title_font_size = 50
        self.draw_title(
            grid.with_focused_window(
                board_location,
                (board_size.x, title_font_size / grid.get_square_pixels()),
                alignY=Align.END,
            ),
            "Tetris",
            title_font_size,
        )

        # --- Left ---

        SIDE_BOARD_WIDTH = 7
        SIDE_BOARD_ITEM_WIDTH = 5

        # Info

        self.draw_items_box(
            grid.with_focused_window(
                board_location - (1, 0), (SIDE_BOARD_WIDTH, 13), alignX=Align.END
            ),
            {
                title: [
                    self.create_item_text(
                        grid.to_pixel_relative((SIDE_BOARD_ITEM_WIDTH, 1)),
                        data,
                        self.color,
                        self.background_color,
                    )
                ]
                for title, data in info.items()
            },
        )

        # Buttons

        self.draw_items_box(
            grid.with_focused_window(
                board_location + (0, board_size.y) - (1, 0),
                (SIDE_BOARD_WIDTH, 7),
                alignX=Align.END,
                alignY=Align.END,
            ),
            {},
        )

        # --- Right ---

        # Queue

        self.draw_items_box(
            grid.with_focused_window(
                board_location + (board_size.x, 0) + (1, 0),
                (SIDE_BOARD_WIDTH, 13),
                alignX=Align.START,
            ),
            {
                "Queue": [
                    self.create_item_piece(grid.get_square_pixels(), piece, (SIDE_BOARD_ITEM_WIDTH, 10/len(queue)))
                    for piece in queue
                ]
            },
        )

        # Held

        self.draw_items_box(
            grid.with_focused_window(
                board_location + board_size + (1, 0), (SIDE_BOARD_WIDTH, 7), alignY=Align.END
            ),
            {
                "Held": [
                    self.create_item_piece(grid.get_square_pixels(), held_piece, (SIDE_BOARD_ITEM_WIDTH, 4))
                ]
            },
        )


def main() -> None:
    import pathlib
    import numpy as np

    pygame.init()

    grid_size = 25

    screen_width = 40
    screen_height = screen_width // 1.618

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        (screen_width * grid_size, screen_height * grid_size)
    )

    grid = GridContext(screen, grid_size)

    assets = pathlib.Path(__file__).parent / "assets"

    pngs = ["I", "J", "L", "O", "S", "T", "Z"]

    tetris = TetrisRenderer(
        TetrominoTiles.from_image_files(
            {
                key + 1: assets / "normal-tetromino" / f"{value}.png"
                for key, value in enumerate(pngs)
            },
            assets / "normal-tetromino" / "default.png",
            0,
        ),
        TetrominoTiles.from_image_files(
            {
                key + 1: assets / "ghost-tetromino" / f"{value}.png"
                for key, value in enumerate(pngs)
            },
            assets / "ghost-tetromino" / "default.png",
            0
        ),
        color="white",
        secondary_color=(50, 50, 50),
        background_color="black",
    )

    board = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 3, 3, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 4, 4, 0, 5, 5, 0, 0, 0, 0],
            [0, 4, 4, 0, 0, 5, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 7, 0],
            [0, 0, 0, 0, 0, 0, 7, 7, 0, 0],
        ]
    )

    info = {"score": "13314", "level": "3", "lines": "38", "time": "2:42"}

    queue = [
        np.array(
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 2, 0],
                [2, 2, 2],
                [0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0],
            ]
        ),
    ]

    held = np.array(
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
        ]
    )

    tetris.draw_tetris(grid, board, info, queue, held)

    while True:
        if pygame.event.get(pygame.QUIT):
            break
        pygame.display.flip()
        clock.tick(25)


if __name__ == "__main__":
    main()
