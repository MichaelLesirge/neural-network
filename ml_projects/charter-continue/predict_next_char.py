import pathlib
import sys

"""Result: unsurprising just always predicts E no matter what"""

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent.parent))

import csv

import numpy as np

import neural_network as nn

# min_char, max_char = ord(" "), ord("~")
min_char, max_char = 0x20, 0x7E

termination_char = "\n"

alphabet_len = ord("Z") - ord("A") + 1

def lower_char_to_num(char: str) -> int:
    if char == termination_char: return 0
    n = ord(char) + 1
    if n > ord("Z"): n -= alphabet_len
    return n - min_char

def num_to_lower_char(n: int) -> str:
    if n == 0: return "\n"
    n += min_char
    if n >= ord("A"): n += alphabet_len
    return chr(n - 1)

def to_one_hot_vector(nums, n_labels: int) -> np.ndarray:
    return np.eye(n_labels)[nums]

def message_to_one_hot(message: str) -> np.ndarray:
    return to_one_hot_vector([lower_char_to_num(char) for char in message], n_different_chars)
    
n_different_chars = lower_char_to_num(chr(max_char)) + 1
n_chars_accepted = 25

hidden_layer_size = 2**10

def format_one_hot_messages(data: np.ndarray) -> np.ndarray:
    data = data[-n_chars_accepted:]
    return np.hstack((np.zeros((max((n_chars_accepted - len(data)), 0), n_different_chars)).flatten(), data.flatten()))

network = nn.network.Network([
    nn.layers.Dense(n_different_chars * n_chars_accepted, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, hidden_layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(hidden_layer_size, n_different_chars),
    nn.activations.Softmax(),    
], loss=nn.losses.CategoricalCrossEntropy())

try:
    network.load_params(str(directory / "mnist-network"))
except FileNotFoundError:
    placers_per_message = 3

    min_message_size = 3
    
    print("Loading Data...")
    
    files = ["dialogueText.csv", "dialogueText_196.csv", "dialogueText_301.csv"]
    with open(directory / "Ubuntu-dialogue-corpus" / files[1], "r", encoding="utf8") as file:
        data = csv.reader(file.readlines())
        next(data, None)
        messages = [row[5].lower().strip() + termination_char for row in data if len(row[5]) > min_message_size and all(min_char < ord(char) <= 0x007E for char in row[5])]
    
    print("Formatting Data...")

    computer_readable_messages = [message_to_one_hot(message) for message in messages]

    X_train = np.empty(shape=(len(computer_readable_messages) * placers_per_message, n_different_chars * n_chars_accepted))
    y_train = np.empty(shape=(len(computer_readable_messages) * placers_per_message, n_different_chars))


    for message_index, message in enumerate(computer_readable_messages):
        for place_index in range(placers_per_message):
            train_index = message_index * placers_per_message + place_index
            
            rand_index = np.random.randint(0, len(message)-1)
                                
            y_train[train_index] = message[rand_index]
            X_train[train_index] = format_one_hot_messages(message[:rand_index])
            
    print("Training...")

    network.train(X_train, y_train, batch_size=16, epochs=1, learning_rate=0.01)
    network.save_params(str(directory / "mnist-network"))

while True:
    message = input("CharGPN> ")
    while message[-1] != termination_char:
        print(message, end="\r")
        output = network.compute(format_one_hot_messages(message_to_one_hot(message)))
        char = num_to_lower_char(output.argmax())
        message += char
    print("\n")