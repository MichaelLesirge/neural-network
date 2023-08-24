import numpy as np
from matplotlib import pyplot as plt

inputs = np.array([-1.0, -2.0, 3.0])
weights = np.array([3.0, -2.0, 1.0])
bias = 1.0

target = np.random.randint(0, 10)
while target == 5: target = np.random.randint(0, 10)

learning_rate = 0.001
iterations = 100

outputs = []
losses = []

print(f"Start: Weights={weights.tolist()}, Bias={bias}")

for i in range(1, iterations + 1):
    # n() is full "network", l() is loss, a() is activation, f() is neuron stuff
    # x is input
    
    # --- Forward ---
    
    # n(x, y) = l(a(f(x)), y)
    
    # standard neuron forward pass inputs * weights + bias
    neuron_output = np.dot(inputs, weights) + bias
    
    # ReLU activation function, 0 for negative values and linear for positive
    relu_output = np.maximum(neuron_output, 0)
    
    # calculate error with MSE
    loss = np.mean(np.square(target - relu_output))
    
    # --- Save data for graphs --- 
    
    losses.append(loss)
    outputs.append(relu_output)
    
    if i == 1:
        print(f"Iteration #0: Loss={loss}, Output={relu_output}, Target={target}")
    
    # --- Backward ---
    
    # chain rule: n'(x, y) = l'(a(f(x)), y) * a'(f(x)) * f'(x)
    
    """
    derivative of MSE
    loss_grad = l'(a(f(x)), y)
    
    p is for y_pred, t is y_true
    l(p, t) = sum((t - p)^2) / len(p)
    
    prime for p parameter
    l'(p, t) = sum(2*(t - p)^(2-1)) / len(p)
    Sum can be ignored because other variables can be treated as constants.
    Imagine p is p1, p2, etc and t is t1, t2, etc, since we only focus on 1 parameter at a time
    the other ones can be treated as just constants and the derivative of a constant is 0.
    Since we do all the calculations for all p values at once we can just ignore them.
    l'(p, t) = 2*(t - p) / len(p)
    """
    loss_grad = 2 * (relu_output - target) / relu_output.size
    
    """
    derivative for ReLU
    relu_grad = loss_grad * a'(f(x))
    
    if x < 0 than the output is a constant (0), and the derivative of a constant is 0
    else the output is x making it linear, and the derivative of x*1 is 1
    """
    relu_grad = loss_grad * (neuron_output > 0).astype(float)
    
    """
    neuron_grad = relu_grad * f'(x)
    
    derivative of layer
    
    f(w, x, b) = w * x + b
    
    prime for x parameter
    b can be treated as constant so its derivative is 0, and x is what w is multiped by so it is its gradient
    f'(w, x, b) = x + 0
    f'(w, x, b) = w
    """
    neuron_grad = relu_grad * weights
    
    """
    f'(w, x, b) = w*x + b
    
    prime for w parameter
    b can be treated as constant so its derivative is 0, and w is what x is multiped by so it is its gradient
    f'(w, x, b) = x
 
    prime for w parameter
    w and x are constant so they can be ignore as their derivative is 0, while b is linear is its derivative is 1 (b = b * 1)
    f'(w, x, b) = 1
    """ 
    weights_grad = relu_grad * inputs
    bias_grad = relu_grad
    
    """multiply grad by learning_rate so it does not change to much and subtract that product since you want to go down the slope (try adding it to see how values run away from target)"""
    weights -= learning_rate * weights_grad
    bias -= learning_rate * bias_grad
    
    if i % (iterations // 10) == 0:
        print(f"Iteration #{i}: Loss={loss}, Output={relu_output}, Target={target}")

print(f"End: Weights={weights.tolist()}, Bias={bias}")

# --- plotting stuff ---

loss_fig, loss_axis = plt.subplots()
loss_axis.plot(range(iterations), losses, label = "loss")
loss_axis.set_ylim(bottom=0)
loss_axis.set_ylabel("Iterations")
loss_axis.set_xlabel("Loss")
loss_axis.set_title("Loss")

data_fig, data_axis = plt.subplots()
data_axis.plot(range(iterations), outputs, label = "output")
data_axis.plot(range(iterations), [target for _ in range(iterations)], label = "target", color = "green")
data_axis.set_ylim(0, 10)
data_axis.set_ylabel("Iterations")
data_axis.set_xlabel("Neuron Output")
data_axis.legend(loc = "best")
data_axis.set_title("Outputs")


plt.show()