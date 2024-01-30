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
    + 2  # current piece x and y
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


_shapes_one_hot = np.eye(len(tetromino.SHAPES))
def game_to_inputs(game: Game) -> np.ndarray:
    return np.concatenate([
        np.array([value is not None for value, (row, col) in game._board], dtype=np.float64).flatten(),
        _shapes_one_hot[tetromino.SHAPES.index(game._board.current_figure.type)],
        np.array([game._board.current_figure.x, game._board.current_figure.y], dtype=np.float64),
    ])
    
def outputs_to_moves(output_array: np.ndarray) -> list[Moves]:
    return [
        outputs[output_array.argmax()]
    ]