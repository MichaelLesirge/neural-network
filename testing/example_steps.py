import numpy as np

# input neurons: 2, output neurons: 3
# pretend all values are decimals not hole numbers, just using ints for simple viewing

inputs = np.array([1, 2])

weights = np.array([[3, 4], [5, 6], [7, 8]])

biases = np.array([9, 10, 11])

def relu(x): return np.maximum(x, 0)
activation = relu

actual = [10, 20, 30]

def mse(true, actual): return np.mean(np.square(true - actual))
error_function = mse

learning_rate = 0.001

# [1, 2] * [[3, 4], [5, 6], [7, 8]]
# [1*3 + 2*4, 1*5 + 2*6, 1*7 + 2*8]
# [3 + 8, 5 + 12, 7 + 16]
# [11, 17, 23]
prediction_weights = np.dot(weights, inputs)
print("inputs * weights =", prediction_weights)
print(f"{inputs.tolist()} * {weights.tolist()} =", prediction_weights)
print()

prediction_biases = prediction_weights + biases
print("inputs * weights + biases =", prediction_biases)
print(f"{prediction_weights.tolist()} + {biases.tolist()} =", prediction_biases)
print()

prediction_activation = relu(prediction_biases)
print("activation(inputs * weights + biases) =", prediction_activation)
print(f"{activation.__name__}({prediction_biases.tolist()}) =", prediction_biases)
print()

error = mse(actual, prediction_activation)
print("error(activation(inputs * weights + biases)) =", error)
print(f"{error_function.__name__}({prediction_activation.tolist()}) =", error)
print()


