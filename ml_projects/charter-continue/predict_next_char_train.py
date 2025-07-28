# Quick project I assumed would fail so bad code quality

import time, os

from network_util import *

import numpy as np

DATA_POINTS_PER_MESSAGE = 1
MIN_MESSAGE_SIZE = 3

EPOCHS = 3
BATCH_SIZE = 16
LEARNING_RATE = 0.0075

OUTPUT_FOLDER = directory / "looped-train"
TRAINING_DATA_PATH = directory / "data" / "dataset" / "data.txt"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("Loading Data...")

LOAD_NETWORK_AT_START = None

if LOAD_NETWORK_AT_START is not None:
    network.load(str(LOAD_NETWORK_AT_START))

with open(TRAINING_DATA_PATH, "r", encoding="utf-8") as file:
    messages = [normalize(line).strip() for line in file.readlines()]
    messages = [message + END_LINE for message in messages if len(message) > MIN_MESSAGE_SIZE]
    
print("Formatting Data...")

computer_readable_messages = [message_to_one_hot(message) for message in messages]

X_train = np.empty(shape=(len(computer_readable_messages) * DATA_POINTS_PER_MESSAGE, NETWORK_INPUT_LAYER_SIZE))
y_train = np.empty(shape=(len(computer_readable_messages) * DATA_POINTS_PER_MESSAGE, NETWORK_OUTPUT_LAYER_SIZE))

print(f"""
        Using {len(computer_readable_messages):,} messages to create {len(X_train):,} data points to train on, repeated {EPOCHS:,} times.
        That is {X_train.nbytes // 2**20:,} MB of data.
        Training happens in batches of {BATCH_SIZE} with a learning rate of {LEARNING_RATE:%}.
    """)

print("Training in loop...")
print("Stop at any round and view result")
print()

for i in range(100):
    print(f"Round {i:,}. Beginning at {time.ctime(time.time())}")

    for message_index, message in enumerate(computer_readable_messages):
        for place_index in range(DATA_POINTS_PER_MESSAGE):
            train_index = message_index * DATA_POINTS_PER_MESSAGE + place_index
            
            rand_index = np.random.randint(MIN_MESSAGE_SIZE - 1, len(message) - 1)
            
            X_train[train_index] = format_one_hot_messages(message[:rand_index])
            y_train[train_index] = message[rand_index]

    network.train(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, learning_rate=LEARNING_RATE)

    network.dump(str(OUTPUT_FOLDER / f"char-network-v{i}"))
    print()
