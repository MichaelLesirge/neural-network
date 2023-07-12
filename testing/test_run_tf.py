import tensorflow as tf
from tensorflow import keras
import numpy as np
from random import randrange

R_MAX = 10

def to_one_hot(x, n_samples: int = None) -> np.ndarray:
    return np.eye(n_samples or np.max(x) + 1)[x]

def format_x_data(a, b, *, r_max):
    return np.hstack(to_one_hot([a, b], r_max))

def format_y_data(c, *, r_max):
    return to_one_hot(c, r_max * 2)

def make_data(amount, r_max = R_MAX):
    xs = np.array([
        [randrange(r_max), randrange(r_max)] for i in range(amount)
    ])

    ys = np.array([
        y for y in np.sum(xs, axis=1)
    ])

    x_one_hot = np.array([format_x_data(a, b, r_max=r_max) for (a, b) in xs], np.float64)
    y_one_hot = np.array([format_y_data(c, r_max=r_max) for c in ys], np.float64)

    return x_one_hot, y_one_hot

x_train, y_train = make_data(10000)
x_test, y_test = make_data(100)

print(x_train.shape, y_train.shape)

# test out my test with tensorflow
model = keras.models.Sequential([
    keras.layers.InputLayer(20),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(20, activation="softmax"),
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

model.fit(x_train, y_train, batch_size=64, epochs=3)
loss, accuracy = model.evaluate(x_test, y_test)

print(f"Accuracy is {accuracy:%}.")

def sort_dict(d):
    sorted_by_values = sorted(d.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_by_values)

while True:
    print()
    a = int(input("a = "))
    b = int(input("b = "))
    (output,) = model.predict(np.array([format_x_data(a, b, r_max=R_MAX)]))

    guesses = sort_dict({n: pred for n, pred in enumerate(output)})
    
    print("\n".join(f"{n}: {pred:%}" for n, pred in guesses.items()))

    print("Guess:", np.argmax(output))