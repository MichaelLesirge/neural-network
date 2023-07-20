import numpy as np

# https://www.haio.ir/app/uploads/2021/12/Neural-Networks-from-Scratch-in-Python-by-Harrison-Kinsley-Daniel-Kukiela-z-lib.org_.pdf

inputs = np.array([[1, 2], [1, 2]])

weights = np.array([[3, 4, 5],
                    [6, 7, 8]])
bias = np.array([0, 0, 0])

output = np.dot(inputs, weights) + bias

print(output)