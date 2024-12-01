import pathlib
import math
from typing import Callable

import numpy as np
import pygame

from game_state import State

from .display import Display
from .tetris_ui import CircleToggleButton, TetrisRenderer, TetrominoTiles, GridContext, TextButton
from .colors import Color

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
    ASSETS_PATH = pathlib.Path(__file__).parent / "tetris_ui" / "assets"

    def __init__(self, tetromino_colors: dict[int, Color]) -> None:
        pygame.init()

        assets = self.ASSETS_PATH

        self.title = "Tetris"

        start_grid_size = pygame.Vector2(25, 25)

        self.screen_width = 40
        self.screen_height = self.screen_width // 1.618

        self.screen = pygame.display.set_mode(
            (self.screen_width * start_grid_size.x, self.screen_height * start_grid_size.y),
            pygame.RESIZABLE,
        )

        pygame.display.set_caption(self.title)

        self.pause_button = CircleToggleButton(
            pygame.image.load(assets / "play.png"),
            pygame.image.load(assets / "pause.png"),
        )

        self.mute_button = CircleToggleButton(
            pygame.image.load(assets / "mute_sound.png"),
            pygame.image.load(assets / "play_sound.png"),
        )

        self.set_up_music()     

        self.resume_button = TextButton("Resume", (255, 255, 255), (50, 50, 50))
        self.restart_button = TextButton("Restart", (255, 255, 255), (50, 50, 50))

        self.tetris = TetrisRenderer()

        default_png = "default.png"
        color_png_map = {
            Color.CYAN: "I.png",
            Color.YELLOW: "O.png",
            Color.PURPLE: "T.png",
            Color.GREEN: "S.png",
            Color.BLUE: "J.png",
            Color.RED: "Z.png",
            Color.ORANGE: "L.png",
        }

        self.tetromino_tiles = TetrominoTiles(
            {
                key: pygame.image.load(assets / "normal-tetromino" / color_png_map.get(value, default_png))
                for key, value in tetromino_colors.items()
            },
            pygame.image.load(assets / "normal-tetromino" / default_png),
            null_tile_value=0,
        )

        self.tetromino_ghost_tiles = TetrominoTiles(
            {
                key: pygame.image.load(assets / "ghost-tetromino" / color_png_map.get(value, default_png))
                for key, value in tetromino_colors.items()                
            },
            pygame.image.load(assets / "ghost-tetromino" / default_png),
            null_tile_value=0,
        )

        self.control_buttons = [self.pause_button, self.mute_button]

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

        self.tetris.set_control_buttons(self.control_buttons)

        self.tetris.set_title(self.title, font="Monospace", scale=2)
        self.tetris.set_text_settings("Berlin Sans FB", scale=1)

        self.tetris.set_outline(3)

    def set_up_music(self) -> None:
        pygame.mixer.music.load(self.ASSETS_PATH / "tetris.mp3") 
        pygame.mixer.music.play(-1, 0, 1000 * 10)

        self.mute_button.add_enabled_action(lambda: pygame.mixer.music.pause())
        self.mute_button.add_disabled_action(lambda: pygame.mixer.music.unpause())

    def add_pause_button_action(self, enable_action: Callable, disable_action: Callable) -> None:
        self.pause_button.add_enabled_action(enable_action)
        self.pause_button.add_disabled_action(disable_action)

        self.resume_button.add_pressed_action(self.pause_button.disable)

    def add_restart_button_action(self, action: Callable) -> None:
        self.restart_button.add_pressed_action(action)
        self.restart_button.add_pressed_action(self.pause_button.disable)

    def update(self, state: State) -> None:

        self.tetris.set_board_shape(state.board.T.shape, (1, 1))

        self.tetris.set_boards([
            (state.board, self.tetromino_tiles),
            (state.current_tetromino_board, self.tetromino_tiles.apply(lambda x: make_transparent(x, (1 - math.sin(state.current_tetromino_percent_placed * math.pi) * 0.5)))),
            (state.ghost_tetromino_board, self.tetromino_ghost_tiles),
        ])

        self.tetris.set_held_tetromino(
            state.held_tetromino,
            (
                self.tetromino_tiles
                if state.can_use_held_tetromino
                else self.tetromino_tiles.apply(gray_scale)
            ),
        )

        self.tetris.set_queued_tetromino(state.tetromino_queue, self.tetromino_tiles)

        self.tetris.set_info(state.info)

        self.tetris.draw(GridContext.create_from_smallest_rows_and_cols(self.screen, (self.screen_width, self.screen_height)))

        mouse_position = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]
        for button in self.control_buttons:
            button.update(mouse_position, mouse_down)
        for button in [self.resume_button, self.restart_button]:
            button.update(mouse_position, mouse_down)

        self.tetris.set_game_over_menu(state.game_over, state.verbose_info.get("score", 0), state.verbose_info.get("high_score", 0), self.restart_button)
        self.tetris.set_pause_menu(state.game_paused, self.resume_button, self.restart_button)


        pygame.display.flip()