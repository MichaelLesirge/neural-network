# --- Path Setup ---

import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent.parent))

# --- Imports ---

import numpy as np

import constants
import neural_network as nn
from tetris import Moves, Game, tetromino

outputs = [
    Moves.LEFT, Moves.RIGHT, Moves.SPIN, None
]

n_inputs = (
    (constants.BOARD_WIDTH * constants.BOARD_HEIGHT)  # flat board
    + len(tetromino.SHAPES)  # one hot current piece type
    + constants.BOARD_WIDTH + constants.BOARD_HEIGHT # one hot X and Y location 
    + tetromino.MAX_ROTATIONS # one hot piece rotation
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

], loss=nn.losses.CategoricalCrossEntropy(categorical_labels=False))


_piece_to_index = dict(((b, a) for (a, b) in enumerate(tetromino.SHAPES)))
_one_hot_shapes = np.eye(len(tetromino.SHAPES), dtype=np.float64)
_one_hot_x = np.eye(constants.BOARD_WIDTH, dtype=np.float64)
_one_hot_y = np.eye(constants.BOARD_HEIGHT, dtype=np.float64) 
_one_hot_rotations = np.eye(tetromino.MAX_ROTATIONS, dtype=np.float64)
def game_to_inputs(game: Game) -> np.ndarray:
    return np.concatenate([
        np.array([value is not None for value, _ in game._board], dtype=np.float64).flatten(), #  board
        _one_hot_shapes[_piece_to_index[game._board.current_figure.type]], # piece type
        _one_hot_x[game._board.current_figure.x], # x
        _one_hot_y[game._board.current_figure.y], # y
        _one_hot_rotations[game._board.current_figure.rotation], # rotation
    ])
    
def outputs_to_moves(output_array: np.ndarray) -> list[Moves]:
    return [
        outputs[output_array.argmax()]
    ]

_one_hot_moves = np.eye(len(outputs), dtype=np.float64)
def moves_to_outputs(moves: list[Moves]) -> np.ndarray:
    return _one_hot_moves[outputs.index(moves[0])]