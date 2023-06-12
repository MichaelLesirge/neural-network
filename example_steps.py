import numpy as np

# input neurons: 2, output neurons: 3
# pretend all values are decimals not hole numbers, just using ints for simple viewing

inputs = np.array([1, 2])

weights = np.array([[3, 4, 5], [6, 7, 8]])

biases = np.array([9, 10, 11])

def relu(x): return np.maximum(x, 0)
activation = relu

actual = [10, 20, 30]

def mse(true, actual): return np.mean(np.square(true - actual))
error_function = mse

learning_rate = 0.001

# [1, 2] * [[3, 4, 5], [6, 7, 8]]
# [1*3 + 2*6, 1*4 + 2*7, 1*5 + 2*8]
# [3 + 12, 4 + 14, 5 + 16]
# [15, 18, 21]

prediction = np.dot(inputs, weights)
print("inputs * weights =", prediction)

# [15, 18, 22] + [15, 18, 21]
# [15 + 9, 18 + 10, 21 + 11]
# [24, 28, 32]
prediction = prediction + biases
print("inputs * weights + biases =", prediction)


# relu([24, 28, 32])
# [max(24, 0), max(28, 0), max(32, 0)])
# [24, 28, 32]
prediction = relu(prediction)
print("activation(inputs * weights + biases) =", prediction)

# mean(([10, 20, 30] - [24, 28, 32]) ^ 2)
# mean(([10-24, 20-28, 30-32]) ^ 2)
# mean(([-14, -8, -2]) ** 2)
# mean(([-14^2, -8^2, -2^2]))
# mean(([196, 64, 4]))

# sum([196, 64, 4]) / len([196, 64, 4])
# 264 / 3
# 88

error = mse(actual, prediction)
print("output_error =", error)


