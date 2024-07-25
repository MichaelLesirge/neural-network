# Quick project I assumed would fail so bad code quality

import csv

from util import *

import numpy as np

DATA_POINTS_PER_MESSAGE = 1
MIN_MESSAGE_SIZE = 3

EPOCHS = 3
BATCH_SIZE = 16
LEARNING_RATE = 0.069
    
print("Loading Data...")

network.load(str(directory / "char-network-first" ))

with open(directory / "data.txt", "r", encoding="utf-8") as file:
    messages = [line + END_LINE for line in file.readlines() if len(line) > MIN_MESSAGE_SIZE]

# files = ["dialogueText.csv", "dialogueText_196.csv", "dialogueText_301.csv"]
# with open(directory / "Ubuntu-dialogue-corpus" / files[1], "r", encoding="utf8") as file:
#     data = csv.reader(file.readlines())
#     next(data, None)
#     messages = [row[5].lower().strip() + end_line for row in data if len(row[5]) > min_message_size and all(min_char < ord(char) <= 0x007E for char in row[5])]
# with open(directory / "data.txt", "r", encoding="utf-8") as file:
#     data = csv.reader(file.readlines())
#     messages = [normalize(line[3]) + end_line for line in data if len(line) > min_message_size]
#     print(messages)
    
print("Formatting Data...")

computer_readable_messages = [message_to_one_hot(message) for message in messages]

X_train = np.empty(shape=(len(computer_readable_messages) * DATA_POINTS_PER_MESSAGE, NETWORK_INPUT_LAYER_SIZE))
y_train = np.empty(shape=(len(computer_readable_messages) * DATA_POINTS_PER_MESSAGE, NETWORK_OUTPUT_LAYER_SIZE))

print(f"""
        Using {len(computer_readable_messages):,} messages to create {len(X_train):,} data points to train on, repeated {EPOCHS:,} times.
        That is {X_train.nbytes // 2**20:,} MB of data.
        Training happens in batches of {BATCH_SIZE} with a learning rate of {LEARNING_RATE:%}.
    """)

for i in range(500):
    print(f"Round {i:,}")

    for message_index, message in enumerate(computer_readable_messages):
        for place_index in range(DATA_POINTS_PER_MESSAGE):
            train_index = message_index * DATA_POINTS_PER_MESSAGE + place_index
            
            rand_index = np.random.randint(MIN_MESSAGE_SIZE - 1, len(message) - 1)
            
            X_train[train_index] = format_one_hot_messages(message[:rand_index])
            y_train[train_index] = message[rand_index]

            
    print("Training...")

    network.train(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, learning_rate=LEARNING_RATE)

    network.dump(str(directory / "mass-train" / f"char-network-v{i}"))
