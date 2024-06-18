from tetris import TetrisGameManager, Grid, ShuffledBagQueue, TetrominoShape

board_size = (10, 20)
board = Grid(board_size)

visible_queue_size = 3

tetromino_shapes = [
    TetrominoShape(
        "I",
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
    ),
    TetrominoShape(
        "O",
        [
            [1, 1],
            [1, 1],
        ],
    ),
    TetrominoShape(
        "L",
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ],
    ),
    TetrominoShape(
        "J",
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
    ),
    TetrominoShape(
        "T",
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
    ),
    TetrominoShape(
        "Z",
        [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ],
    ),
    TetrominoShape(
        "S",
        [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ],
    ),
]

piece_queue = ShuffledBagQueue(tetromino_shapes, visible_queue_size)

game_manager = TetrisGameManager(board, piece_queue)