import pygame

from tetris import Action
from tetris_ui import TetrisRenderer, TetrominoTiles, ToggleButton, assets
from .player import Player

class PygamePlayer(Player):
    def __init__(self) -> None:
        pygame.init()

        # Constants

        TITLE = "Tetris"

        START_GRID_SIZE = pygame.Vector2(25, 25)

        SCREEN_WIDTH = 40
        SCREEN_HEIGHT = SCREEN_WIDTH // 1.618

        # Pygame objects

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH * START_GRID_SIZE.x, SCREEN_HEIGHT * START_GRID_SIZE.y),
            pygame.RESIZABLE,
        )

        pygame.display.set_caption(TITLE)

        # Buttons

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

        self.buttons = [pause_button, mute_button]

        # Tiles

        PNGs = ["I", "J", "L", "O", "S", "T", "Z"]

        self.tetromino_tiles = TetrominoTiles.from_image_files(
                {
                    key + 1: assets / "normal-tetromino" / f"{value}.png"
                    for key, value in enumerate(PNGs)
                },
                assets / "normal-tetromino" / "default.png",
                null_tile_value=0,
            )

        self.tetromino_ghost_tiles = TetrominoTiles.from_image_files(
                {
                    key + 1: assets / "ghost-tetromino" / f"{value}.png"
                    for key, value in enumerate(PNGs)
                },
                assets / "ghost-tetromino" / "default.png",
                null_tile_value=0,
            )


        # tetris.set_colors(
        #     color = (255, 255, 255),
        #     secondary_color = (50, 50, 50),
        #     background_color = (0, 0, 0),
        # )
        # # tetris.set_colors(
        # #     color = "cyan",
        # #     secondary_color = "purple",
        # #     background_color = "dark blue",
        # # )

        # tetris.set_control_buttons(
        #     buttons
        # )

        # tetris.set_title(TITLE.title(), font="Monospace", scale=2)
        # tetris.set_text_settings("Berlin Sans FB", scale=1)

        # tetris.set_outline(3)

        # grey_scale_tetromino_tiles = tetromino_tiles.apply(gray_scale)

    
    def get_name(self) -> str:
        return "User"
    
    def get_actions(self) -> list[Action]:
        return []