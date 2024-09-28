import numpy as np

from . import (
    TetrisGameManager,
    Grid,
    ShuffledBagQueue,
    TetrominoShape,
    LevelManager,
    ScoreManger,
    TimeManager,
    Event,
)

NULL_VALUE = 0

board = Grid.empty(shape=(10, 20), null_value=NULL_VALUE)

tetromino_shapes = [
    TetrominoShape(
        "I",
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        null_value=NULL_VALUE
    ),
    TetrominoShape(
        "O",
        [
            [1, 1],
            [1, 1],
        ],
        null_value=NULL_VALUE
    ),
    TetrominoShape(
        "L",
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE
    ),
    TetrominoShape(
        "J",
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE
    ),
    TetrominoShape(
        "T",
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE
    ),
    TetrominoShape(
        "Z",
        [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE
    ),
    TetrominoShape(
        "S",
        [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE
    ),
]

piece_queue = ShuffledBagQueue(tetromino_shapes, visible_size = 3)

level_manager = LevelManager(
    lines_for_next_level = 10,
)

score_manager = ScoreManger(
    for_line_clear = [0, 40, 100, 300, 1200],
    for_events = {Event.SOFT_DROP: 1, Event.HARD_DROP: 2}
)

time_manager = TimeManager(
    fps = 60
)

game_manager = TetrisGameManager(board, piece_queue)