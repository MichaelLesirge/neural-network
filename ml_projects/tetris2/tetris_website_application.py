from game_state import State
from player import AlgorithmPlayer

from display import Color
from model import TetrominoShape, TetrisWebsiteGame

NULL_VALUE = 0

tetromino_shapes = [
    TetrominoShape(
        "I", Color.CYAN,
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "O", Color.YELLOW,
        [
            [1, 1],
            [1, 1],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "L", Color.ORANGE,
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "J", Color.BLUE,
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "T", Color.PURPLE,
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "Z", Color.RED,
        [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "S", Color.GREEN,
        [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
]

player = AlgorithmPlayer(tetromino_shapes, null_value=NULL_VALUE)
model = TetrisWebsiteGame(tetromino_shapes, null_value=NULL_VALUE)

model.setup()

actions = []

while True:    
    model.update(actions)

    game_state = State(
        model.get_board(),
        model.get_piece_board(),
        0,
        [[]],
        None,
        False,
        [],
        {},
        {},
        False,
        False,
        0
    )

    actions = player.get_actions(game_state)