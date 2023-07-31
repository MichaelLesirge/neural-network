import numpy as np

"""
Dot product of two arrays. Specifically,

- If both `a` and `b` are 1-D arrays, it is inner product of vectors
    (without complex conjugation).

- If both `a` and `b` are 2-D arrays, it is matrix multiplication,
    but using matmul or a @ b is preferred.

- If either `a` or `b` is 0-D (scalar), it is equivalent to multiply using multiply or a * b is preferred.

- If `a` is an N-D array and `b` is a 1-D array, it is a sum product over the last axis of `a` and `b`.

- If `a` is an N-D array and `b` is an M-D array (where M>=2), it is a
    sum product over the last axis of `a` and the second-to-last axis of `b`

Only works if the last dimension of `a` is the same size as the second-to-last dimension of `b`.
"""

# The width of `a` must be the same as the height `b`.
# 'a' sets the height and 'b' sets the width


x = np.array([[1, 2, 3]])
y = np.array([[4, 5, 6]])

print(x.shape, y.T.shape, x.T.shape[-1] == y.shape[-2])
print(np.dot(x, y.T))
"""
[[1, 2, 3]] * [[4],
               [5],
               [6]]

[[1*4 + 2*5 + 3*6]]

[[4 + 10 + 18]]

[[32]]
"""
print()

print(x.T.shape, y.shape, x.T.shape[-1] == y.shape[-2])
print(np.dot(x.T, y))
# [[1], [2], [3]] * [[4, 5, 6]]
# [[1*4, 2*4, 3*4], [[1*5, 2*5, 3*5]], [[1*6, 2*6, 3*6]]]
# [[4, 8, 12], [5, 10, 15], [6, 12, 18]]
print()

# different shape with T in back
x = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]])
y = np.array([[4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6]])
print(x.shape, y.T.shape, x.shape[-1] == y.T.shape[-2])
print(np.dot(x, y.T))
print()

# same shape with T in front
print(x.T.shape, y.shape, x.T.shape[-1] == y.shape[-2])
print(np.dot(x.T, y))
print()