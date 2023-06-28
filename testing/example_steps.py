import numpy as np

# input neurons: 2, output neurons: 3
# pretend all values are decimals not hole numbers, just using ints for simple viewing

inputs = np.array([1, 2])

weights = np.array([[3, 4, 5], [6, 7, 8]])

biases = np.array([9, 10, 11])

def relu(x): return np.maximum(x, 0)
activation_function = relu

actual = [10, 20, 30]

def mse(true, actual): return np.mean(np.square(true - actual))
error_function = mse

# [1, 2] * [[3, 4, 5], [6, 7, 8]]
# [1*3 + 2*6, 1*4 + 2*7, 1*5 + 2*8]
# [3 + 12, 4 + 14, 5 + 16]
# [15, 18, 21]
prediction_step_1 = np.dot(inputs, weights)
print("inputs * weights =", prediction_step_1)
print(f"{inputs.tolist()} * {weights.tolist()} =", prediction_step_1)
print()

# [15, 18, 22] + [15, 18, 21]
# [15 + 9, 18 + 10, 21 + 11]
# [24, 28, 32]
prediction_step_2 = prediction_step_1 + biases
print("inputs * weights + biases =", prediction_step_2)
print(f"{prediction_step_1.tolist()} + {biases.tolist()} =", prediction_step_2.tolist())
print()


# relu([24, 28, 32])
# [max(24, 0), max(28, 0), max(32, 0)])
# [24, 28, 32]
prediction_step_3 = activation_function(prediction_step_2)
print("activation(inputs * weights + biases) =", prediction_step_3)
print(f"{activation_function.__name__}({prediction_step_2.tolist()}) =", prediction_step_3.tolist())
print()

# mean(([10, 20, 30] - [24, 28, 32]) ^ 2)
# mean(([10-24, 20-28, 30-32]) ^ 2)
# mean(([-14, -8, -2]) ** 2)
# mean(([-14^2, -8^2, -2^2]))
# mean(([196, 64, 4]))

# sum([196, 64, 4]) / len([196, 64, 4])
# 264 / 3
# 88

error = error_function(actual, prediction_step_3)
print("error(activation(inputs * weights + biases)) =", error)
print(f"{error_function.__name__}({prediction_step_3.tolist()}) =", error)
print()


