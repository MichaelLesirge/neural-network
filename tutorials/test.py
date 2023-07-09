import numpy as np
from matplotlib import pyplot as plt
from random import randrange

"""Horrible code, just meant to test out stuff"""

R_MAX = 10

def to_one_hot(x, n_samples: int = None) -> np.ndarray:
    return np.eye(n_samples or np.max(x) + 1)[x]

inputs = np.array([
    [randrange(R_MAX), randrange(R_MAX)] for i in range(20)
])

actual = np.array([
    y for y in np.sum(inputs, axis=1)
])

inputs_one_hot = np.array([np.hstack(to_one_hot(row, R_MAX)) for row in inputs], np.float64)
actual_one_hot = np.array([(to_one_hot(row, R_MAX * 2)) for row in actual], np.float64)

weights1 = np.random.rand(R_MAX * 2, 16)
weights2 = np.random.rand(16, 16)
weights3 = np.random.rand(16, R_MAX * 2)

gradient_biases1 = np.zeros(16)
gradient_biases2 = np.zeros(16)
gradient_biases3 = np.zeros(R_MAX * 2)

def relu(x): return np.maximum(x, 0)
def relu_grad(x): return (x > 0).astype(int)

def sigmoid(x): return 1 / (1 + np.exp(-x))
def sigmoid_grad(x): return sigmoid(x) * (1-sigmoid(x))

def softmax(x):
    exp_x = np.exp(x - x.max(axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)
def softmax_grad(x):
    x = x.reshape(-1,1)
    return np.diagflat(x) - np.dot(x, x.T)


def mean_squared_error(y_true, y_pred): return np.mean(np.square(y_true - y_pred))
def categorical_cross_entropy(y_true, y_pred): return np.mean(-np.sum(y_true * np.log(np.clip(y_pred, 1e-7, 1-1e-7))))

learning_rate = 0.1
epochs = 3
mini_batch_size = 64

print([len(x) for x in np.array_split(actual_one_hot, mini_batch_size)])

errors = []
for epoch_count in range(epochs):
    gradient_weight1 = 0
    gradient_weight2 = 0
    gradient_weight3 = 0
    
    gradient_biases1 = 0
    gradient_biases2 = 0
    gradient_biases3 = 0
    
    for batch_inputs, batch_actual, in zip(np.array_split(inputs_one_hot, mini_batch_size), np.array_split(actual_one_hot, mini_batch_size)):
        activations1 = sigmoid(np.dot(batch_inputs, weights1) + gradient_biases1)
        activations2 = sigmoid(np.dot(activations1, weights2) + gradient_biases2)
        activations3 = softmax(np.dot(activations2, weights3) + gradient_biases3)

        output = activations3
        
        error = categorical_cross_entropy(batch_actual, output)
        errors.append(error)
        
        # change the zeros here
        gradient_weight3 += 0
        gradient_weight2 += 0
        gradient_weight1 += 0
        
        gradient_biases3 += 0
        gradient_biases2 += 0
        gradient_biases1 += 0

    weights3 += learning_rate * -gradient_weight3
    weights2 += learning_rate * -gradient_weight2
    weights1 += learning_rate * -gradient_weight1
    gradient_biases3 += learning_rate * -gradient_biases3
    gradient_biases2 += learning_rate * -gradient_biases2
    gradient_biases1 += learning_rate * -gradient_biases1

plt.plot(errors)
plt.show()