import pathlib
import sys

"""Result: unsurprising just always predicts the most common letter, e"""

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent.parent))

import numpy as np
np.seterr(all='raise')

import neural_network as nn

end_line = "\n"
termination_chars = {end_line}

fallback_char = ""
min_char, max_char = ord(" "), ord("~")

max_chars_in_data = 25
n_different_chars = max_char - min_char + 1

def char_to_num(char: str) -> int:
    n = ord(char)
    if char in termination_chars:
        return 0
    if not min_char <= n <= max_char:
        return char_to_num(fallback_char)
    return n - min_char + 1


def num_to_lower_char(n: int) -> str:
    if n == 0:
        return end_line
    return chr(n + min_char - 1)


def to_one_hot_vector(nums, n_labels: int) -> np.ndarray:
    return np.eye(n_labels)[nums]

def message_to_one_hot(message: str) -> np.ndarray:
    return to_one_hot_vector([char_to_num(char) for char in message], n_different_chars)

hidden_layer_size = 2**10

def format_one_hot_messages(data: np.ndarray) -> np.ndarray:
    data = data[-max_chars_in_data:]
    padding = np.zeros([max_chars_in_data - len(data), n_different_chars]).flatten()
    return np.hstack([padding, data.flatten()])

network = nn.network.Network([
    nn.layers.Dense(n_different_chars * max_chars_in_data, hidden_layer_size),
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
    network.load(str(directory / "char-network"))
except FileNotFoundError:
# if (True):
#     network.load(str(directory / "char-network"))

    placers_per_message = 6
    min_message_size = 3
    
    print("Loading Data...")
    
    # files = ["dialogueText.csv", "dialogueText_196.csv", "dialogueText_301.csv"]
    # with open(directory / "Ubuntu-dialogue-corpus" / files[1], "r", encoding="utf8") as file:
    #     data = csv.reader(file.readlines())
    #     next(data, None)
    #     messages = [row[5].lower().strip() + termination_char for row in data if len(row[5]) > min_message_size and all(min_char < ord(char) <= 0x007E for char in row[5])]

    with open(directory / "data.txt", "r", encoding="utf-8") as file:
        messages = [line + end_line for line in file.readlines() if len(line) > min_message_size]
    
    print("Formatting Data...")

    computer_readable_messages = [message_to_one_hot(message) for message in messages]

    X_train = np.empty(shape=(len(computer_readable_messages) * placers_per_message, n_different_chars * max_chars_in_data))
    y_train = np.empty(shape=(len(computer_readable_messages) * placers_per_message, n_different_chars))

    for message_index, message in enumerate(computer_readable_messages):
        for place_index in range(placers_per_message):
            train_index = message_index * placers_per_message + place_index
            
            rand_index = np.random.randint(min_message_size - 1, len(message) - 1)
            
            X_train[train_index] = format_one_hot_messages(message[:rand_index])
            y_train[train_index] = message[rand_index]

            
    print("Training...")

    network.train(X_train, y_train, batch_size=16, epochs=3, learning_rate=0.0862)
    network.dump(str(directory / "char-network"))

CHOOSE_FROM_TOP = 2

if CHOOSE_FROM_TOP is None:
    print("Choose next character based on random choice with probabilities")
elif CHOOSE_FROM_TOP == 1:
    print("Choose next character based on highest probability")
else:
    print(f"Choose next character based on random choice from top {CHOOSE_FROM_TOP} with probabilities")
    

while True:
    message = input("CharGPN> ")

    print(message, end="")

    while len(message) == 0 or message[-1] not in termination_chars:
        output = network.compute(format_one_hot_messages(message_to_one_hot(message)))[0]

        top_indices = np.argsort(output)[-(CHOOSE_FROM_TOP if CHOOSE_FROM_TOP is not None else len(output)):]
        top_probabilities = output[top_indices]
        normalized_probabilities = top_probabilities / top_probabilities.sum()
        selected = np.random.choice(top_indices, p=normalized_probabilities)

        char = num_to_lower_char(selected)
        print(char, end="")

        message += char
    print("\n")
