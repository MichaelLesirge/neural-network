import pathlib

import numpy as np
import pygame

from game_state import State

from .display import Display
from .tetris_ui import ToggleButton, TetrisRenderer, TetrominoTiles, GridContext


def gray_scale(surface: pygame.Surface) -> pygame.Surface:
    array = pygame.surfarray.array3d(surface)
    # luminosity filter
    averages = [
        [(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in array
    ]
    array = np.array([[[avg, avg, avg] for avg in col] for col in averages])
    return pygame.surfarray.make_surface(array)


def make_transparent(surface: pygame.Surface, opacity: float = 1) -> pygame.Surface:
    alpha = int(opacity * 255)
    new_surface = surface.copy()
    new_surface.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    return new_surface


class PygameDisplay(Display):

    def __init__(self, tetromino_names: dict[int, str]) -> None:
        pygame.init()

        self.title = "Tetris"

        start_grid_size = pygame.Vector2(25, 25)

        self.screen_width = 40
        self.screen_height = self.screen_width // 1.618

        self.screen = pygame.display.set_mode(
            (self.screen_width * start_grid_size.x, self.screen_height * start_grid_size.y),
            pygame.RESIZABLE,
        )

        pygame.display.set_caption(self.title)

        assets = pathlib.Path(__file__).parent / "tetris_ui" / "assets"

        pause_button = ToggleButton(
            pygame.image.load(assets / "play.png"),
            pygame.image.load(assets / "pause.png"),
        )

        pause_button.add_enabled_action(lambda: print("Pause"))
        pause_button.add_disabled_action(lambda: print("Play"))

        mute_button = ToggleButton(
            pygame.image.load(assets / "mute_sound.png"),
            pygame.image.load(assets / "play_sound.png"),
        )

        mute_button.add_enabled_action(lambda: print("Mute"))
        mute_button.add_disabled_action(lambda: print("Play"))

        self.tetris = TetrisRenderer()

        self.tetromino_tiles = TetrominoTiles(
            {
                key: pygame.image.load(assets / "normal-tetromino" / value)
                for key, value in tetromino_names.items()
            },
            pygame.image.load(assets / "normal-tetromino" / "default.png"),
            null_tile_value=0,
        )

        self.tetromino_ghost_tiles = TetrominoTiles(
            {
                key: pygame.image.load(assets / "ghost-tetromino" / value)
                for key, value in tetromino_names.items()                
            },
            pygame.image.load(assets / "ghost-tetromino" / "default.png"),
            null_tile_value=0,
        )

        self.buttons = [pause_button, mute_button]

        self.tetris.set_colors(
            color=(255, 255, 255),
            secondary_color=(50, 50, 50),
            background_color=(0, 0, 0),
        )
        # tetris.set_colors(
        #     color = "cyan",
        #     secondary_color = "purple",
        #     background_color = "dark blue",
        # )

        self.tetris.set_control_buttons(self.buttons)

        self.tetris.set_title(self.title, font="Monospace", scale=2)
        self.tetris.set_text_settings("Berlin Sans FB", scale=1)

        self.tetris.set_outline(3)

    def update(self, state: State) -> None:

        self.tetris.set_board_shape(state.board.T.shape, (1, 1))

        self.tetris.set_boards([
            (state.board, self.tetromino_tiles),
            (state.ghost_tetromino_board, self.tetromino_ghost_tiles),
            (state.current_tetromino_board, self.tetromino_tiles.apply(lambda tile: make_transparent(tile, state.current_tetromino_percent_placed)))
        ])

        self.tetris.set_held_tetromino(
            state.held_tetromino,
            (
                self.tetromino_tiles.apply(gray_scale)
                if state.can_use_held_tetromino
                else self.tetromino_tiles
            ),
        )

        self.tetris.set_queued_tetromino(state.tetromino_queue, self.tetromino_tiles)

        self.tetris.set_info(state.info)

        self.tetris.draw(GridContext.create_from_smallest_rows_and_cols(self.screen, (self.screen_width, self.screen_height)))

        mouse_position = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]
        for button in self.buttons:
            button.update(mouse_position, mouse_down)
            

        pygame.display.flip()