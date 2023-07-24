import numpy as np
from matplotlib import pyplot as plt

inputs = np.array([1.0, -2.0, 3.0])
weights = np.random.randn((3))
bias = 1

target = 15

learning_rate = 0.001

iterations = 200

losses = []
outputs = []

for i in range(iterations):
    output_nn = np.dot(inputs, weights) + bias
    output_relu = np.maximum(output_nn, 0)
    
    outputs.append(output_relu)
    
    loss = abs(output_relu - target)
    
    grad_next = output_relu - target
    
        
    grad_relu = grad_next * (output_nn > 0).astype(float)
    grad_nn = output_relu * grad_relu
    
    weights -= learning_rate * grad_nn
    
    if i % (iterations // 10) == 0: print(f"#{i}: output = {output_relu}, loss = {loss}")
    losses.append(loss)

print((weights, bias))

# plt.title("Error")  
# plt.plot(range(iterations), losses)

plt.title("Value")
plt.plot(range(iterations), outputs)
plt.ylim(bottom = 0)

plt.show()
