import pathlib, sys
import unicodedata

import numpy as np

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent.parent))

import neural_network as nn

END_LINE = "\n"
TERMINATION_CHARS = {END_LINE}
FALLBACK_CHAR = " "

MIN_CHAR, MAX_CHAR = ord(" "), ord("~")
NUMBER_OF_CHARS_IN_RANGE = MAX_CHAR - MIN_CHAR + 1

MAX_CHARS_IN_DATA = 25

def char_to_num(char: str) -> int:
    n = ord(char)
    if char in TERMINATION_CHARS:
        return 0
    if not MIN_CHAR <= n < MAX_CHAR:
        return char_to_num(FALLBACK_CHAR)
    return n - MIN_CHAR + 1

def num_to_lower_char(n: int) -> str:
    if n == 0:
        return END_LINE
    return chr(n + MIN_CHAR - 1)

def normalize(message: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', message)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def to_one_hot_vector(nums, n_labels: int) -> np.ndarray:
    return np.eye(n_labels)[nums]

def message_to_one_hot(message: str) -> np.ndarray:
    return to_one_hot_vector([char_to_num(char) for char in message], NUMBER_OF_CHARS_IN_RANGE)

def format_one_hot_messages(data: np.ndarray) -> np.ndarray:
    data = data[-MAX_CHARS_IN_DATA:]
    padding = np.zeros([MAX_CHARS_IN_DATA - len(data), NUMBER_OF_CHARS_IN_RANGE]).flatten()
    return np.hstack([padding, data.flatten()])

NETWORK_INPUT_LAYER_SIZE = NUMBER_OF_CHARS_IN_RANGE * MAX_CHARS_IN_DATA
NETWORK_HIDDEN_LAYER_SIZE = 2**10
NETWORK_OUTPUT_LAYER_SIZE = NUMBER_OF_CHARS_IN_RANGE

network = nn.network.Network([
    nn.layers.Dense(NETWORK_INPUT_LAYER_SIZE, NETWORK_HIDDEN_LAYER_SIZE),
    nn.activations.ReLU(),
    
    nn.layers.Dense(NETWORK_HIDDEN_LAYER_SIZE, NETWORK_HIDDEN_LAYER_SIZE),
    nn.activations.ReLU(),

    nn.layers.Dense(NETWORK_HIDDEN_LAYER_SIZE, NETWORK_HIDDEN_LAYER_SIZE),
    nn.activations.ReLU(),

    nn.layers.Dense(NETWORK_HIDDEN_LAYER_SIZE, NETWORK_HIDDEN_LAYER_SIZE),
    nn.activations.ReLU(),
    
    nn.layers.Dense(NETWORK_HIDDEN_LAYER_SIZE, NUMBER_OF_CHARS_IN_RANGE),
    nn.activations.Softmax(),    
], loss=nn.losses.CategoricalCrossEntropy())