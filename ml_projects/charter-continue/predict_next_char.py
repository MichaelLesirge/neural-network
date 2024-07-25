# Quick project I assumed would fail so bad code quality

import pathlib
import sys
import csv
import unicodedata

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent.parent))

import numpy as np
np.seterr(all='raise')

import neural_network as nn

end_line = "\n"
termination_chars = {end_line}

fallback_char = " "
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

def normalize(message: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', message)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

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

    placers_per_message = 6
    min_message_size = 3

    epochs = 3
    batch_size = 16
    learning_rate = 0.2
    
    print("Loading Data...")
    
    # files = ["dialogueText.csv", "dialogueText_196.csv", "dialogueText_301.csv"]
    # with open(directory / "Ubuntu-dialogue-corpus" / files[1], "r", encoding="utf8") as file:
    #     data = csv.reader(file.readlines())
    #     next(data, None)
    #     messages = [row[5].lower().strip() + end_line for row in data if len(row[5]) > min_message_size and all(min_char < ord(char) <= 0x007E for char in row[5])]

    # with open(directory / "data.txt", "r", encoding="utf-8") as file:
    #     messages = [line + end_line for line in file.readlines() if len(line) > min_message_size]

    with open(directory / "data.txt", "r", encoding="utf-8") as file:
        data = csv.reader(file.readlines())
        messages = [normalize(line[3]) + end_line for line in data if len(line) > min_message_size]
        print(messages)
        
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

    print(f"""
          Using {len(computer_readable_messages)} messages to create {len(X_train)} data points to train on, repeated {epochs} times.
          Training happens in batches of {batch_size} with a learning rate of {learning_rate:%}.
          That is {X_train.nbytes * 1e+6} MB of data.
        """)

    network.train(X_train, y_train, batch_size=batch_size, epochs=epochs, learning_rate=learning_rate)
    network.dump(str(directory / "char-network"))

CHOOSE_FROM_TOP = 5

if CHOOSE_FROM_TOP is None:
    print("Choose next character based on random choice with probabilities")
elif CHOOSE_FROM_TOP == 1:
    print("Choose next character based on highest probability")
else:
    print(f"Choose next character based on random choice from top {CHOOSE_FROM_TOP} with probabilities")
print()    

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
    print()
