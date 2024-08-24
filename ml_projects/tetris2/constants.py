import numpy as np

from tetris import (
    TetrisGameManager,
    Grid,
    ShuffledBagQueue,
    TetrominoShape,
    LevelManager,
    ScoreManger,
    TimeManager,
    Action,
)

from game import Game

DTYPE = np.uint8
NULL_VALUE = 0

board = Grid.empty(shape=(10, 20), null_value=NULL_VALUE, dtype=DTYPE)

tetromino_shapes = [
    TetrominoShape(
        "I",
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        null_value=NULL_VALUE, dtype=DTYPE
    ),
    TetrominoShape(
        "O",
        [
            [1, 1],
            [1, 1],
        ],
        null_value=NULL_VALUE, dtype=DTYPE
    ),
    TetrominoShape(
        "L",
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE, dtype=DTYPE
    ),
    TetrominoShape(
        "J",
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE, dtype=DTYPE
    ),
    TetrominoShape(
        "T",
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE, dtype=DTYPE
    ),
    TetrominoShape(
        "Z",
        [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE, dtype=DTYPE
    ),
    TetrominoShape(
        "S",
        [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE, dtype=DTYPE
    ),
]

piece_queue = ShuffledBagQueue(tetromino_shapes, visible_size = 3)

level_manager = LevelManager(
    lines_for_next_level = 10,
)

score_manager = ScoreManger(
    for_line_clear = [0, 40, 100, 300, 1200],
    for_action = {Action.SOFT_DROP: 1, Action.HARD_DROP: 2}
)

time_manager = TimeManager(
    fps = 60
)

game_manager = TetrisGameManager(board, piece_queue)