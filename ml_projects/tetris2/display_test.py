import pygame
import numpy as np

from tetris_ui import TetrisRenderer, TetrominoTiles, ToggleButton, GridContext

def gray_scale(surface: pygame.Surface) -> pygame.Surface:
    array = pygame.surfarray.array3d(surface)
    #luminosity filter
    averages = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in array]
    array = np.array([[[avg,avg,avg] for avg in col] for col in averages])
    return pygame.surfarray.make_surface(array)

def make_transparent(surface: pygame.Surface, opacity: float = 1) -> pygame.Surface:
    alpha = int(opacity * 255)
    new_surface = surface.copy()
    new_surface.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    return new_surface


def main() -> None:
    """For demo purposes, making sure it works"""

    import pathlib
    import numpy as np

    pygame.init()

    title = "Tetris"

    start_grid_size = pygame.Vector2(25, 25)

    screen_width = 40
    screen_height = screen_width // 1.618

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        (screen_width * start_grid_size.x, screen_height * start_grid_size.y),
        pygame.RESIZABLE,
    )

    pygame.display.set_caption(title)


    assets = pathlib.Path(__file__).parent / "tetris_ui" / "assets"

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

    tetris = TetrisRenderer()

    tetromino_tiles = TetrominoTiles.from_image_files(
            {
                key + 1: assets / "normal-tetromino" / f"{value}.png"
                for key, value in enumerate(pngs)
            },
            assets / "normal-tetromino" / "default.png",
            null_tile_value=0,
        )

    tetromino_ghost_tiles = TetrominoTiles.from_image_files(
            {
                key + 1: assets / "ghost-tetromino" / f"{value}.png"
                for key, value in enumerate(pngs)
            },
            assets / "ghost-tetromino" / "default.png",
            null_tile_value=0,
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

    current_board = np.array(
        [
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

    scale = 0.5
    d_scale = 0.01
    
    buttons = [pause_button, mute_button]

    tetris.set_board_shape(board.T.shape, (1, 1))

    tetris.set_colors(
        color = (255, 255, 255),
        secondary_color = (50, 50, 50),
        background_color = (0, 0, 0),
    )
    # tetris.set_colors(
    #     color = "cyan",
    #     secondary_color = "purple",
    #     background_color = "dark blue",
    # )

    tetris.set_control_buttons(
        buttons
    )

    tetris.set_title("Tetris", font="Monospace", scale=2)
    tetris.set_text_settings("Berlin Sans FB", scale=1)

    tetris.set_outline(3)

    grey_scale_tetromino_tiles = tetromino_tiles.apply(gray_scale)

    while True:

        # Fade
        scale += d_scale

        if scale > 1 - d_scale:
            scale = 0.9
            d_scale = -abs(d_scale)

        if scale < d_scale:
            scale = 0.1
            d_scale = abs(d_scale)

        # Tetris

        tetris.set_held_tetromino(held, tetromino_tiles if scale > 0.5 else grey_scale_tetromino_tiles)
        tetris.set_queued_tetromino(queue, tetromino_tiles)
        tetris.set_info(info)

        tetris.set_boards([
            (board, tetromino_tiles),
            (ghost_board, tetromino_ghost_tiles),
            (current_board, tetromino_tiles.apply(lambda tile: make_transparent(tile, scale)))
        ])

        tetris.draw(GridContext.create_from_smallest_rows_and_cols(screen, (screen_width, screen_height)))

        # Buttons
        mouse_position = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]
        pressed = mouse_down and not was_mouse_down
        for button in buttons:
            button.update(mouse_position, pressed)
        was_mouse_down = mouse_down

        # Quit
        if pygame.event.get(pygame.QUIT):
            break

        # Next Frame
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()