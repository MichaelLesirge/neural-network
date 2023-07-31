import numpy as np
from matplotlib import pyplot as plt

# 3 inputs -> 2 outputs

inputs = np.array([[-1.0, -2.0, 3.0]])

weights = np.array([[3.0, -2.0],
                    [2.0, -2.0],
                    [-1.0, 0.5]])

bias = np.array([1.0, 1.0])

targets = np.random.randint(0, 10, size=(1, 2))
while targets[0][0] == targets[0][1]: targets = np.random.randint(0, 10, size=(2))

learning_rate = 0.001
iterations = 300

outputs = []
losses = []

print(f"Start: Weights={weights.tolist()}, Bias={bias.tolist()}")

for i in range(1, iterations + 1):
    
    # --- forward ---
    
    # n(x) = l(f(x, w, b), y)
    
    # f(x, w, b)
    output = np.dot(inputs, weights) + bias
    
    # l(f(x, w, b), y)
    loss = np.mean(np.square(output - targets))
    
    # --- Save data for graphs --- 
    
    if i == 1:
        print(f"Iteration #0: Loss={loss}, Output={output.tolist()}, Target={targets.tolist()}")
    
    outputs.append(output)
    losses.append(loss)
    
    # --- backward ---
    
    # n'(x) = l'(f(x, w, b), y) * f'(x, w, b)
    
    # loss_grad = l'(f(x, w, b), y)
    loss_grad = 2 * (output - targets) / output.size
        
    # loss_grad * f'(x, w, b) for x
    # loss_grad * weights
    inputs_grad = np.dot(loss_grad, weights.T)
    # [[1, 2]] * [[3, 4, 5], [6, 7, 8]] = 
    # [1*3 + 2*6, 1*4 + 2*7, 1*5 + 2*8] = 
    # [15, 18, 21], shape is same as inputs now
    
    # loss_grad * f'(x, w, b) for w
    # loss_grad * inputs
    weights_grad = np.dot(inputs.T, loss_grad)
    # [[3], [4], [5]] * [[1, 2]] = 
    # [[3*1, 3*2], [4*1, 4*2], [5*1, 5*2]] =
    # [[3, 6], [4, 8], [5, 10]], shape is same as weights now
    
    # loss_grad * f(x, w, b) for b
    # loss_grad
    bias_grad = np.sum(loss_grad, axis=0, keepdims=True)
    # sum columns
    # [[1, 2]], same shape as biases
    
    weights -= learning_rate * weights_grad
    bias_grad -= learning_rate * bias_grad
    
    if i % (iterations // 10) == 0:
        print(f"Iteration #{i}: Loss={loss}, Output={output.tolist()}, Target={targets}")

print(f"End: Weights={weights.tolist()}, Bias={bias.tolist()}")

# --- plotting stuff ---

loss_fig, loss_axis = plt.subplots()
loss_axis.plot(range(iterations), losses, label = "loss")
loss_axis.set_ylim(bottom=0)
loss_axis.set_ylabel("Iterations")
loss_axis.set_xlabel("Loss")
loss_axis.set_title("Loss")

data_fig, data_axis = plt.subplots()
data_axis.plot(range(iterations), [output[0][0] for output in outputs], label = "output1", color = "royalblue")
data_axis.plot(range(iterations), [output[0][1] for output in outputs], label = "output2", color = "darkblue")
data_axis.plot(range(iterations), [targets[0][0] for _ in range(iterations)], label = "target1", color = "lime")
data_axis.plot(range(iterations), [targets[0][1] for _ in range(iterations)], label = "target2", color = "darkgreen")
# data_axis.set_ylim(0, 10)
data_axis.set_ylabel("Iterations")
data_axis.set_xlabel("Layer outputs compared to targets")
data_axis.legend(loc = "best")
data_axis.set_title("Outputs")


plt.show()