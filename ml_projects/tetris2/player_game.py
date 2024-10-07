import pygame

from model import BasicModel, tetris
from view import View
from player import PygamePlayer
from ui import PygameDisplay
from presenter import Presenter
from game_actions import Action

def main() -> None:

    NULL_VALUE = 0

    # Model

    board = tetris.Grid.empty(shape=(10, 20), null_value=NULL_VALUE)

    tetromino_shapes = [
        tetris.TetrominoShape(
            "I",
            [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ],
            null_value=NULL_VALUE
        ),
        tetris.TetrominoShape(
            "O",
            [
                [1, 1],
                [1, 1],
            ],
            null_value=NULL_VALUE
        ),
        tetris.TetrominoShape(
            "L",
            [
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0],
            ],
            null_value=NULL_VALUE
        ),
        tetris.TetrominoShape(
            "J",
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0],
            ],
            null_value=NULL_VALUE
        ),
        tetris.TetrominoShape(
            "T",
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0],
            ],
            null_value=NULL_VALUE
        ),
        tetris.TetrominoShape(
            "Z",
            [
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0],
            ],
            null_value=NULL_VALUE
        ),
        tetris.TetrominoShape(
            "S",
            [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0],
            ],
            null_value=NULL_VALUE
        ),
    ]

    piece_queue = tetris.ShuffledBagQueue(tetromino_shapes, visible_size=3)

    level_manager = tetris.LevelManager(
        lines_for_next_level=10,
    )

    score_manager = tetris.ScoreManger(
        for_line_clear=[0, 40, 100, 300, 1200],
        for_events={tetris.Event.SOFT_DROP: 1, tetris.Event.HARD_DROP: 2}
    )

    time_manager = tetris.TimeManager(
        fps=60
    )

    model = BasicModel(board, piece_queue)

    # View

    player = PygamePlayer({
        pygame.K_UP: Action.SPIN,
        pygame.K_DOWN: Action.SOFT_DROP,
        pygame.K_SPACE: Action.HARD_DROP,
        pygame.K_LEFT: Action.LEFT,
        pygame.K_RIGHT: Action.RIGHT,
        pygame.K_c: Action.HOLD,
    })

    display = PygameDisplay()

    view = View(player, display)

    # Presenter

    presenter = Presenter(model, view)

    presenter.run()


if __name__ == "__main__":
    main()
