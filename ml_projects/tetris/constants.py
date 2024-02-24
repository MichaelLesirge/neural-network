BOARD_WIDTH, BOARD_HEIGHT = 10, 20

# --- Path Setup ---

import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent.parent))

# --- Imports ---

import numpy as np

import constants
import neural_network as nn
from tetris import Move, Tetris, TetrominoShape

POTENTIAL_MOVES: list[Move] = [
    Move.LEFT, Move.RIGHT, Move.SPIN, None
]

STATE_SIZE = (    
    (constants.BOARD_WIDTH * constants.BOARD_HEIGHT)  # flat board
    + len(TetrominoShape.ALL_SHAPES)  # one hot current piece type
    + constants.BOARD_WIDTH + constants.BOARD_HEIGHT # one hot X and Y location 
    + TetrominoShape.MAX_ROTATIONS # one hot piece rotation
)

_LAYER_SIZE = 8 ** 2  # 64
 
NETWORK = nn.network.Network([
    nn.layers.Dense(STATE_SIZE, _LAYER_SIZE),
    nn.activations.ReLU(),

    nn.layers.Dense(_LAYER_SIZE, _LAYER_SIZE),
    nn.activations.ReLU(),
    
    nn.layers.Dense(_LAYER_SIZE, _LAYER_SIZE),
    nn.activations.ReLU(),
    
    nn.layers.Dense(_LAYER_SIZE, 1),
    nn.activations.Linear(),

], loss=nn.losses.MSE())

VERSION = 6
SAVE_FILE_NAME = str(directory / ("tetris_model" + ("" if VERSION is None else f"_{VERSION}")))