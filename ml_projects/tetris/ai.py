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

potential_moves: list[Move] = [
    Move.LEFT, Move.RIGHT, Move.SPIN, None
]

state_size = (    
    (constants.BOARD_WIDTH * constants.BOARD_HEIGHT)  # flat board
    + len(TetrominoShape.ALL_SHAPES)  # one hot current piece type
    + constants.BOARD_WIDTH + constants.BOARD_HEIGHT # one hot X and Y location 
    + TetrominoShape.MAX_ROTATIONS # one hot piece rotation
)

layer_size = 8 ** 2  # 64
 
network = nn.network.Network([
    nn.layers.Dense(state_size, layer_size),
    nn.activations.ReLU(),

    nn.layers.Dense(layer_size, layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(layer_size, layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(layer_size, 1),
    nn.activations.Linear(),

], loss=nn.losses.MSE())

save_file_name = str(directory / "tetris_model")

def save():
    network.dump(save_file_name)

def load():
    network.load(save_file_name)