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

piece_queue = ShuffledBagQueue(tetromino_shapes, visible_size=3)

level_manager = LevelManager(
    lines_for_next_level = 10,
)

score_manager = ScoreManger(
    [0, 40, 100, 300, 1200]
    {Action.SOFT_DROP: 1, Action.HARD_DROP: 2}
)

game_manager = TetrisGameManager(board, piece_queue, level_manager)

def main() -> None:
    import random

    for i in range(10):
        action = random.choice(list(Action))
        print(i, action)
        game_manager.step([action])
        gb = game_manager.board.copy()
        gb.insert(game_manager.falling_tetromino.get_position(), game_manager.falling_tetromino.get_grid_array())
        print(gb)
        print()

if __name__ == "__main__":
    main()