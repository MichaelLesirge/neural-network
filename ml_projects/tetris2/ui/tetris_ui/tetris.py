import pygame

from .grid import GridContext, Align
from .tiles import Tiles
from .button import ToggleButton
from ._common import ColorValue, Size

from typing import Self

Grid = list[list[int]]

def _get_grid_size(grid: Grid) -> pygame.Vector2:
    height = len(grid)
    width = height and len(grid[0])
    return pygame.Vector2(width, height)


# View Render
class TetrisRenderer:
    def __init__(self) -> None:
        self.set_board_shape()
        self.set_boards()
        self.set_colors()
        self.set_control_buttons()
        self.set_held_tetromino()
        self.set_info()
        self.set_outline()
        self.set_queued_tetromino()
        self.set_text_settings()
        self.set_title()

    # --- Stateless drawing methods ----

    def _draw_items_box(
        self, grid: GridContext, padding=1, title: str = None
    ) -> GridContext:
        grid.fill(self.secondary_color)
        grid.outline(self.outline_thickness_pixels, self.outline_color)

        offset = pygame.Vector2(padding, padding)
        inner_grid = grid.with_focused_window(offset, grid.get_size() - offset * 2)

        if title is not None:
            self._draw_item_title(
                inner_grid.with_focused_window(
                    (0, 0), (inner_grid.get_size().x, self.text_scale)
                ),
                title,
            )
            inner_grid = inner_grid.with_focused_window((0, self.text_scale), None)

        return inner_grid

    def _draw_board(self, grid: GridContext, shape: Size, cell_size: Size):

        grid.outline(self.outline_thickness_pixels, self.outline_color)

        grid_cell = pygame.Surface(grid.to_pixel_relative(cell_size), pygame.SRCALPHA)
        pygame.draw.rect(
            grid_cell,
            self.secondary_color,
            pygame.Rect((0, 0), grid_cell.get_size()),
            width=1,
        )

        for x in range(int(shape.x)):
            for y in range(int(shape.y)):
                grid.blit(grid_cell, (x, y))

    def _draw_tetromino_grid(
        self,
        grid: GridContext,
        tetromino: Grid,
        tetromino_tiles: Tiles,
        size: Size = (1, 1),
    ) -> None:

        for position in grid:
            grid.blit(tetromino_tiles.get_tile(tetromino[position.y][position.x], size=grid.to_pixel_relative(size)), position)
            
    def _draw_item_text(
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
            round(grid.get_size().y * grid.get_pixels_cell_size().y),
            False,
            False,
        )
        text_surface = font.render(text, True, color)

        grid.blit(
            text_surface,
            grid.get_size() / 2,
            alignX=Align.CENTER,
            alignY=Align.CENTER,
        )

    def _draw_item_title(self, grid: GridContext, title: str) -> None:
        self._draw_item_text(
            grid,
            title.upper(),
            self.color,
            None,
        )

    def _create_title(
        self, title: str, font_size: int, font_name="Monospace"
    ) -> pygame.Surface:
        title_font = pygame.font.SysFont(font_name, int(font_size), True, False)
        title_surface = title_font.render(title, True, self.color)
        return title_surface

    def _draw_info(
        self,
        grid: GridContext,
        info: dict[str, str],
        text_size: int,
        vertical_gap: int = 0,
    ) -> None:

        height = 0

        box_size = pygame.Vector2(grid.get_size().x, text_size)

        for title, data in info.items():
            self._draw_item_title(
                grid.with_focused_window((0, height), box_size), title
            )
            height += box_size.y

            self._draw_item_text(
                grid.with_focused_window((0, height), box_size),
                data,
                self.color,
                self.background_color,
            )
            height += box_size.y

            height += vertical_gap

    def _draw_buttons(
        self, grid: GridContext, buttons: list[ToggleButton]
    ) -> ToggleButton:

        if len(buttons) == 0:
            return

        x_split = grid.get_size().x / len(buttons)
        y = grid.get_size().y / 2

        for i, button in enumerate(buttons):
            button.put_at_position(
                grid.surface,
                grid.to_pixel_relative_position((x_split * i + x_split / 2, y)),
                grid.get_pixels_cell_size().y * 2,
            )

    def _draw_tetrominoes(
        self,
        grid: GridContext,
        tetrominoes: list[Grid],
        tetromino_tiles: Tiles,
    ) -> None:
        if len(tetrominoes) == 0:
            return

        x = grid.get_size().x / 2
        y_split = grid.get_size().y / len(tetrominoes)

        for i, tetromino in enumerate(tetrominoes):

            size = _get_grid_size(tetromino)

            self._draw_tetromino_grid(
                grid.with_focused_window(
                    (x, y_split * i + y_split / 2),
                    size,
                    alignX=Align.CENTER,
                    alignY=Align.CENTER,
                ),
                tetromino,
                tetromino_tiles,
            )

    def set_colors(
        self,
        color: ColorValue = (255, 255, 255),
        background_color: ColorValue = (0, 0, 0),
        secondary_color: ColorValue = (50, 50, 50),
    ) -> Self:
        self.color = color
        self.secondary_color = secondary_color
        self.background_color = background_color
        return self

    def set_title(self, title: str = None, font: str = "Monospace", scale: float = 1) -> Self:
        self.title = self.__class__.__name__.title() if title is None else title
        self.title_font = font
        self.title_scale = scale
        return self

    def set_outline(self, pixel_width: int = 1, color: ColorValue = None) -> Self:
        self.outline_thickness_pixels = pixel_width
        self.outline_color = color or self.color
        return self

    def set_text_settings(self, font: str = "Monospace", scale: float = 1) -> Self:
        self.font = font
        self.text_scale = scale
        return self

    def set_board_shape(self, shape: Size = (10, 20), cell_size=(1, 1)) -> Self:
        self.board_shape = pygame.Vector2(shape)
        self.board_cell_size = pygame.Vector2(cell_size)
        return self

    def set_boards(self, boards: list[tuple[Grid, Tiles]] = []) -> Self:
        self.boards = boards
        for board, tetromino_tiles in self.boards:
            assert _get_grid_size(board) == self.board_shape, ValueError(
                f"Board shape must be set board shape of {self.board_shape}"
            )
        return self

    def set_queued_tetromino(
        self, queue: list[Grid] = [], tetromino_tiles: Tiles = None
    ) -> Self:
        self.queued_tetromino = queue
        self.queued_tetromino_tiles = tetromino_tiles
        return self

    def set_held_tetromino(
        self, held: Grid = None, tetromino_tiles: Tiles = None
    ) -> Self:
        self.held_tetromino = held
        self.held_tetromino_tiles = tetromino_tiles
        return self

    def set_info(self, info: dict[str, str] = {}) -> Self:
        self.info = info
        return self

    def set_control_buttons(self, buttons: list[ToggleButton] = []) -> Self:
        self.buttons = buttons
        return self

    def draw(
        self,
        grid: GridContext,
    ) -> None:

        # --- Full ---

        grid.fill(self.background_color)

        # --- Center ---

        title_surface = self._create_title(
            self.title,
            self.title_scale * grid.get_pixels_cell_size().y,
            self.title_font,
        )
        title_height = title_surface.get_height() / grid.get_pixels_cell_size().y

        # Board
        board_size = self.board_shape.elementwise() * self.board_cell_size
        board_location = (grid.get_size() - board_size) / 2 + (0, title_height / 4)
        board_grid = grid.with_focused_window(board_location, board_size)

        self._draw_board(board_grid, self.board_shape, self.board_cell_size)

        for board, tetromino_tiles in self.boards:
            self._draw_tetromino_grid(board_grid, board, tetromino_tiles)

        # Title
        inner_title_grid = grid.with_focused_window(
            board_location,
            (board_size.x, title_height),
            alignY=Align.END,
        )
        inner_title_grid.blit(
            title_surface,
            inner_title_grid.get_size() / 2,
            alignX=Align.CENTER,
            alignY=Align.CENTER,
        )

        # ----- Side Panels -----

        SIDE_BOARD_WIDTH = 7

        UPPER_SIDE_BOARD_HEIGHT = 13
        LOWER_SIDE_BOARD_HEIGHT = 7

        SIDE_BOARD_PADDING = 1

        # --- Left ---

        # Info

        inner_info_grid = self._draw_items_box(
            grid.with_focused_window(
                board_location - (1, 0),
                (SIDE_BOARD_WIDTH, UPPER_SIDE_BOARD_HEIGHT),
                alignX=Align.END,
            ),
            padding=SIDE_BOARD_PADDING,
        )
        self._draw_info(
            inner_info_grid,
            self.info,
            text_size=self.text_scale,
            vertical_gap=SIDE_BOARD_PADDING,
        )

        # Buttons

        inner_control_grid = self._draw_items_box(
            grid.with_focused_window(
                board_location + (0, board_size.y) - (1, 0),
                (SIDE_BOARD_WIDTH, LOWER_SIDE_BOARD_HEIGHT),
                alignX=Align.END,
                alignY=Align.END,
            ),
            padding=SIDE_BOARD_PADDING,
            title="controls",
        )
        inner_control_grid.fill(self.background_color)
        self._draw_buttons(inner_control_grid, self.buttons)

        # --- Right ---

        # Queue

        inner_queue_grid = self._draw_items_box(
            grid.with_focused_window(
                board_location + (board_size.x, 0) + (1, 0),
                (SIDE_BOARD_WIDTH, UPPER_SIDE_BOARD_HEIGHT),
                alignX=Align.START,
            ),
            padding=SIDE_BOARD_PADDING,
            title="queue",
        )
        inner_queue_grid.fill(self.background_color)
        self._draw_tetrominoes(
            inner_queue_grid, self.queued_tetromino, self.queued_tetromino_tiles
        )

        # Held

        inner_held_grid = self._draw_items_box(
            grid.with_focused_window(
                board_location + board_size + (1, 0),
                (SIDE_BOARD_WIDTH, LOWER_SIDE_BOARD_HEIGHT),
                alignY=Align.END,
            ),
            padding=SIDE_BOARD_PADDING,
            title="held",
        )
        inner_held_grid.fill(self.background_color)
        self._draw_tetrominoes(
            inner_held_grid,
            [] if self.held_tetromino is None else [self.held_tetromino],
            self.held_tetromino_tiles,
        )
