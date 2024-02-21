# --- Path Setup ---

import pathlib
import sys

from ml_projects.tetris.tetris import shapes

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent.parent))

# --- Imports ---

import numpy as np

import constants
import neural_network as nn
from tetris import Moves, Tetris

outputs = [
    Moves.LEFT, Moves.RIGHT, Moves.SPIN, None
]

n_inputs = (
    (constants.BOARD_WIDTH * constants.BOARD_HEIGHT)  # flat board
    + len(shapes.SHAPES)  # one hot current piece type
    + constants.BOARD_WIDTH + constants.BOARD_HEIGHT # one hot X and Y location 
    + shapes.MAX_ROTATIONS # one hot piece rotation
)

n_outputs = len(outputs)

layer_size = 8 ** 2  # 64
 
network = nn.network.Network([
    nn.layers.Dense(n_inputs, layer_size),
    nn.activations.ReLU(),

    nn.layers.Dense(layer_size, layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(layer_size, layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(layer_size, n_outputs),
    nn.activations.Softmax(),

], loss=nn.losses.CategoricalCrossEntropy(categorical_labels=True))


_piece_to_index = dict(((b, a) for (a, b) in enumerate(shapes.SHAPES)))
_one_hot_shapes = np.eye(len(shapes.SHAPES), dtype=np.float64)
_one_hot_x = np.eye(constants.BOARD_WIDTH, dtype=np.float64)
_one_hot_y = np.eye(constants.BOARD_HEIGHT, dtype=np.float64) 
_one_hot_rotations = np.eye(shapes.MAX_ROTATIONS, dtype=np.float64)
def game_to_inputs(board: Tetris) -> np.ndarray:
    return np.concatenate([
        np.array([value is not None for value, _ in board], dtype=np.float64).flatten(), #  board
        _one_hot_shapes[_piece_to_index[board.current_tetromino.shape]], # piece type
        _one_hot_x[board.current_tetromino.x], # x
        _one_hot_y[board.current_tetromino.y], # y
        _one_hot_rotations[board.current_tetromino.orientation], # rotation
    ])
    
def outputs_to_moves(output_array: np.ndarray) -> list[Moves]:
    return [
        outputs[output_array.argmax()]
    ]

_move_to_index = dict((b, a) for (a, b) in enumerate(outputs))
def moves_to_labels(moves: list[Moves]) -> np.ndarray:
    moves = [move for move in moves if move in outputs] or [None]
    return _move_to_index[moves[-1]]