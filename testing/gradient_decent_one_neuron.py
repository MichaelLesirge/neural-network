import numpy as np
from matplotlib import pyplot as plt

inputs = np.array([1.0, -2.0, 3.0])
weights = np.array([-3.0, -1.0, 2.0])
bias = 1.0

target = 15

learning_rate = 0.001

iterations = 50

losses = []

for i in range(iterations):
    # f(a(x))
    output_nn = np.dot(inputs, weights) + bias
    output_relu = np.maximum(output_nn, 0)
    
    
    loss = abs(output_relu - target)
    
    grad_next = output_relu - target
    
    if i % (iterations // 10) == 0 or i == iterations-1: print(f"#{i}: output = {output_relu}, loss = {loss}")
    losses.append(loss)
        
    grad_relu = grad_next * (output_nn > 0).astype(float)
    grad_nn = (weights * output_relu) * grad_relu
    
    weights -= learning_rate * grad_nn
    
plt.plot(range(iterations), losses)
plt.ylim(bottom = 0)
plt.show()
