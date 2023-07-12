import numpy as np
from random import randrange
from layers import Dense
from activations import ReLU, Softmax

R_MAX = 10


def to_one_hot(x, n_samples: int = None) -> np.ndarray:
    return np.eye(n_samples or np.max(x) + 1)[x]


def format_x_data(a, b, *, r_max):
    return np.hstack(to_one_hot([a, b], r_max))


def format_y_data(c, *, r_max):
    return to_one_hot(c, r_max * 2)


def make_data(amount, r_max=R_MAX):
    xs = np.array([
        [randrange(r_max), randrange(r_max)] for i in range(amount)
    ])

    ys = np.array([
        y for y in np.sum(xs, axis=1)
    ])

    x_one_hot = np.array([format_x_data(a, b, r_max=r_max)
                         for (a, b) in xs], np.float64)
    y_one_hot = np.array([format_y_data(c, r_max=r_max)
                         for c in ys], np.float64)

    return x_one_hot, y_one_hot

def predict(network, input):
    output = input
    for layer in network:
        output = layer.forward(output)
    return output

def train(network, loss, loss_prime, x_train, y_train, epochs = 1000, learning_rate = 0.01, verbose = True):
    for e in range(epochs):
        error = 0
        for x, y in zip(x_train, y_train):
            # forward
            output = predict(network, x)

            # error
            error += loss(y, output)

            # backward
            grad = loss_prime(y, output)
            for layer in reversed(network):
                grad = layer.backward(grad, learning_rate)

        error /= len(x_train)
        if verbose:
            print(f"{e + 1}/{epochs}, error={error}")
            
network = [
    Dense(20, 24, ReLU()),
    Dense(24, 24, ReLU()),
    Dense(24, 20, Softmax()),
]

x_train, y_train = make_data(10000)

x_train = x_train.reshape(x_train.shape + (1, ))
y_train = y_train.reshape(y_train.shape + (1, ))

# x_test, y_test = make_data(100)

print(x_train.shape)

def binary_cross_entropy(y_true, y_pred):
    return np.mean((-y_true * np.log(y_pred)) - (1 - y_true) * np.log(1 - y_pred))

def binary_cross_entropy_prime(y_true, y_pred):
    return (((1 - y_true) / (1 - y_pred)) - (y_true / y_pred)) / np.size(y_true, axis=-1)

train(network, binary_cross_entropy, binary_cross_entropy_prime, x_train, y_train)

def sort_dict(d):
    sorted_by_values = sorted(d.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_by_values)


while True:
    print()
    a = int(input("a = "))
    b = int(input("b = "))
    (output,) = predict(network, np.array([format_x_data(a, b, r_max=R_MAX)]))

    guesses = sort_dict({n: pred for n, pred in enumerate(output)})

    print("\n".join(f"{n}: {pred:%}" for n, pred in guesses.items()))

    print("Guess:", np.argmax(output))
