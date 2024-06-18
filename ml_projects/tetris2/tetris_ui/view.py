import pygame

from grid import GridContext, Align
from tetromino import TetrominoTiles
from button import ToggleButton

xyPair = tuple[int, int] | pygame.Vector2
ColorValue = tuple[int, int, int] | str
Grid = list[list[int]]

def _get_grid_size(grid: Grid) -> pygame.Vector2:
    height = len(grid)
    width = height and len(grid[0])
    return pygame.Vector2(width, height)

# View Render
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

    def draw_items_box(
        self, grid: GridContext, padding=1, title: str = None, title_height: int = 0
    ) -> GridContext:
        grid.fill(self.secondary_color)
        grid.outline(self.outline_width, self.color)

        offset = pygame.Vector2(padding, padding)
        inner_grid = grid.with_focused_window(offset, grid.get_grid_size() - offset * 2)

        if title is not None:
            self.draw_item_title(
                inner_grid.with_focused_window(
                    (0, 0), (inner_grid.get_grid_size().x, title_height)
                ),
                title,
            )
            inner_grid = inner_grid.with_focused_window((0, title_height), None)

        return inner_grid

    def draw_tetrominos_grid(
        self,
        grid: GridContext,
        board: Grid,
        show_grid=False,
        tetrominos: TetrominoTiles = None
    ) -> None:
        
        if tetrominos is None:
            tetrominos = self.tetrominos

        sqaure_size = grid.to_pixel_relative((1, 1))

        squares = tetrominos.get_tetroino_tiles(board, grid.get_square_pixels())

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

    def draw_item_text(
        self,
        grid: GridContext,
        text: str,
        color: ColorValue,
        background: ColorValue = None,
        font_font="Berlin Sans FB",
    ) -> None:

        if background:
            grid.fill(background)

        font = pygame.font.SysFont(
            font_font,
            round(grid.get_grid_size().y * grid.get_square_pixels()),
            False,
            False,
        )
        text_surface = font.render(text, True, color)

        grid.blit(
            text_surface,
            grid.get_grid_size() / 2,
            alignX=Align.CENTER,
            alignY=Align.CENTER,
        )

    def draw_board(self, grid: GridContext, board: Grid, ghost_board: Grid):
        self.draw_tetrominos_grid(
            grid,
            board,
            show_grid=True,
            tetrominos=self.tetrominos
        )
        self.draw_tetrominos_grid(
            grid,
            ghost_board,
            show_grid=False,
            tetrominos=self.ghost_tetrominos
        )
        grid.outline(self.outline_width, self.color)

    def draw_item_title(self, grid: GridContext, title: str) -> None:
        self.draw_item_text(
            grid,
            title.upper(),
            self.color,
            None,
        )

    def create_title(
        self, title: str, font_size: int, font_name="Monospace"
    ) -> pygame.Surface:
        title_font = pygame.font.SysFont(font_name, int(font_size), True, False)
        title_surface = title_font.render(title, True, self.color)
        return title_surface

    def draw_info(
        self,
        grid: GridContext,
        info: dict[str, str],
        text_size: int,
        verticle_gap: int = 0,
    ) -> None:

        height = 0

        box_size = pygame.Vector2(grid.get_grid_size().x, text_size)

        for title, data in info.items():
            self.draw_item_title(grid.with_focused_window((0, height), box_size), title)
            height += box_size.y

            self.draw_item_text(
                grid.with_focused_window((0, height), box_size),
                data,
                self.color,
                self.background_color,
            )
            height += box_size.y

            height += verticle_gap

    def draw_buttons(self, grid: GridContext, buttons: list[ToggleButton]) -> ToggleButton:
        grid.fill(self.background_color)

        if len(buttons) == 0:
            return

        x_split = grid.get_grid_size().x / len(buttons)
        y = grid.get_grid_size().y / 2

        for i, button in enumerate(buttons):
            button.put_at_position(grid.surface, grid.to_pixel_relative_position((x_split * i + x_split / 2, y)), grid.get_square_pixels() * 2)


    def draw_pieces(self, grid: GridContext, queue: list[Grid]) -> None:
        grid.fill(self.background_color)

        if len(queue) == 0:
            return

        x = grid.get_grid_size().x / 2
        y_split = grid.get_grid_size().y / len(queue)

        for i, board in enumerate(queue):

            size = _get_grid_size(board)

            self.draw_tetrominos_grid(
                grid.with_focused_window(
                    (x, y_split * i + y_split / 2),
                    size,
                    alignX=Align.CENTER,
                    alignY=Align.CENTER,
                ),
                board,
            )

    def draw_tetris(
        self,
        grid: GridContext,
        title: str,
        board: Grid,
        ghost_board: Grid,
        info: dict[str, str],
        queued_tetriminos: list[Grid],
        held_tetrimino: Grid,
        held_is_usable: bool,
        buttons: list[ToggleButton],
        *,
        text_box_size = 1
    ) -> pygame.Surface:

        # --- Full ---

        grid.fill(self.background_color)

        # --- Center ---

        title_surface = self.create_title(
            title,
            text_box_size * 2 * grid.get_square_pixels(),
        )
        title_height = title_surface.get_height() / grid.get_square_pixels()

        # Board
        board_size = _get_grid_size(board)
        board_location = (grid.get_grid_size() - board_size) / 2 + (0, title_height / 4)
        self.draw_board(
            grid.with_focused_window(board_location, board_size),
            board,
            ghost_board
        )

        # Title
        inner_title_grid = grid.with_focused_window(
            board_location,
            (board_size.x, title_height),
            alignY=Align.END,
        )
        inner_title_grid.blit(
            title_surface,
            inner_title_grid.get_grid_size() / 2,
            alignX=Align.CENTER,
            alignY=Align.CENTER,
        )

        # ----- Side Panals -----

        SIDE_BOARD_WIDTH = 7

        UPPER_SIDE_BOARD_HEIGHT = 13
        LOWER_SIDE_BOARD_HEIGHT = 7

        SIDE_BOARD_PADDING = 1

        # --- Left ---

        # Info

        inner_info_grid = self.draw_items_box(
            grid.with_focused_window(
                board_location - (1, 0), (SIDE_BOARD_WIDTH, UPPER_SIDE_BOARD_HEIGHT), alignX=Align.END
            ),
            padding=SIDE_BOARD_PADDING,
        )
        self.draw_info(
            inner_info_grid,
            info,
            text_size=text_box_size,
            verticle_gap=SIDE_BOARD_PADDING,
        )

        # Buttons

        inner_control_grid = self.draw_items_box(
            grid.with_focused_window(
                board_location + (0, board_size.y) - (1, 0),
                (SIDE_BOARD_WIDTH, LOWER_SIDE_BOARD_HEIGHT),
                alignX=Align.END,
                alignY=Align.END,
            ),
            padding=SIDE_BOARD_PADDING,
            title="controls",
            title_height=text_box_size,
        )
        self.draw_buttons(
            inner_control_grid,
            buttons
        )

        # --- Right ---

        # Queue

        inner_queue_grid = self.draw_items_box(
            grid.with_focused_window(
                board_location + (board_size.x, 0) + (1, 0),
                (SIDE_BOARD_WIDTH, UPPER_SIDE_BOARD_HEIGHT),
                alignX=Align.START,
            ),
            padding=SIDE_BOARD_PADDING,
            title="queue",
            title_height=text_box_size,
        )
        self.draw_pieces(
            inner_queue_grid,
            queued_tetriminos,
        )

        # Held

        inner_held_grid = self.draw_items_box(
            grid.with_focused_window(
                board_location + board_size + (1, 0),
                (SIDE_BOARD_WIDTH, LOWER_SIDE_BOARD_HEIGHT),
                alignY=Align.END,
            ),
            padding=SIDE_BOARD_PADDING,
            title="held",
            title_height=text_box_size,
        )
        self.draw_pieces(inner_held_grid, [] if held_tetrimino is None else [held_tetrimino])
        if not held_is_usable:
            inner_held_grid.outline(-1, "red")


def main() -> None:
    """For demo purposes, making sure it works"""

    import pathlib
    import numpy as np

    pygame.init()

    title = "Tetris"

    start_grid_size = 25

    screen_width = 40
    screen_height = screen_width // 1.618

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        (screen_width * start_grid_size, screen_height * start_grid_size),
        pygame.RESIZABLE,
    )

    pygame.display.set_caption(title)


    assets = pathlib.Path(__file__).parent / "assets"

    pngs = ["I", "J", "L", "O", "S", "T", "Z"]

    pause_button = ToggleButton(
        pygame.image.load(assets / "play.png"),
        pygame.image.load(assets / "pause.png")
    )
    
    pause_button.add_enabled_action(lambda: print("Pause"))
    pause_button.add_disabled_action(lambda: print("Play"))

    mute_button = ToggleButton(
        pygame.image.load(assets / "mute_sound.png"),
        pygame.image.load(assets / "play_sound.png"),
    )

    mute_button.add_enabled_action(lambda: print("Mute"))
    mute_button.add_disabled_action(lambda: print("Play"))

    tetris = TetrisRenderer(
        TetrominoTiles.from_image_files(
            {
                key + 1: assets / "normal-tetromino" / f"{value}.png"
                for key, value in enumerate(pngs)
            },
            assets / "normal-tetromino" / "default.png",
            empty_tile_key=0,
        ),
        TetrominoTiles.from_image_files(
            {
                key + 1: assets / "ghost-tetromino" / f"{value}.png"
                for key, value in enumerate(pngs)
            },
            assets / "ghost-tetromino" / "default.png",
            empty_tile_key=0,
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 4, 0, 0, 6, 0, 7, 7, 0, 0],
            [0, 4, 0, 6, 6, 0, 5, 7, 1, 0],
            [4, 4, 3, 6, 2, 2, 5, 5, 1, 0],
            [3, 3, 3, 3, 2, 2, 5, 3, 1, 0],
            [1, 3, 3, 3, 5, 3, 3, 3, 1, 0],
            [1, 3, 3, 5, 5, 5, 4, 4, 4, 0],
            [1, 4, 3, 5, 5, 5, 7, 7, 4, 0],
        ],
        dtype=np.uint8,
    )

    ghost_board = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        dtype=np.uint8,
    )

    info = {"score": "13314", "level": "3", "lines": "38", "time": "2:42"}

    queue = [
        np.array(
            [
                [1, 1, 1, 1],
            ]
        ),
        np.array(
            [
                [0, 2, 0],
                [2, 2, 2],
            ]
        ),
        np.array(
            [
                [0, 1, 1],
                [1, 1, 0],
            ]
        ),
    ]

    held = np.array(
        [
            [1, 1, 1, 1],
        ]
    )

    can_use_held = True

    while True:
        grid = GridContext.create_from_smallest_size(screen, (screen_width, screen_height))

        buttons = [pause_button, mute_button]
        tetris.draw_tetris(grid, title, board, ghost_board, info, queue, held, can_use_held, buttons)

        mouse_position = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]
        pressed = mouse_down and not was_mouse_down
        for button in buttons:
            button.update(mouse_position, pressed)
        was_mouse_down = mouse_down

        if pygame.event.get(pygame.QUIT):
            break
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
