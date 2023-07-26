import numpy as np
from matplotlib import pyplot as plt

# 10/10 book would recommend: https://nnfs.io/

def create_data(samples, classes):
    X = np.zeros((samples*classes, 2))
    y = np.zeros(samples*classes, dtype='uint8')
    for class_number in range(classes):
        ix = range(samples*class_number, samples*(class_number+1))
        r = np.linspace(0.0, 1, samples)
        t = np.linspace(class_number*4, (class_number+1)*4, samples) + np.random.randn(samples)*0.2
        X[ix] = np.c_[r*np.sin(t*2.5), r*np.cos(t*2.5)]
        y[ix] = class_number
    return X, y


X, y = create_data(samples=100, classes=3)

# plt.scatter(X[:,0], X[:,1], c = y, cmap="brg")
# plt.show()

class LayerDense:
    def __init__(self, n_inputs, n_outputs) -> None:
        self.weights = np.random.randn(n_inputs, n_outputs) * 0.01
        self.bias = np.zeros(n_outputs)

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.bias

class ActivationReLU:
    def forward(self, inputs):
        self.output = np.maximum(inputs, 0)
    
class ActivationSoftmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        self.output = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        
class LossCategoricalCrossEntropy:
    def calculate(self, output_y, y):
        sample_losses = self.forward(output_y, y)
        
        data_loss = np.mean(sample_losses)
        
        return data_loss

    def forward(self, y_pred, y_true):
        y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
        
        if len(y_true.shape) == 1:
            correct_confidences = y_pred[range(len(y_pred)), y_true]
        
        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(y_pred * y_true, axis=1)
        
        return -np.log(correct_confidences)

dense1 = LayerDense(2, 3)
activation1 = ActivationReLU()

dense2 = LayerDense(3, 3)
activation2 = ActivationSoftmax()

dense1.forward(X)
activation1.forward(dense1.output)

dense2.forward(activation1.output)
activation2.forward(dense2.output)

output = activation2.output

loss_func = LossCategoricalCrossEntropy()

loss = loss_func.calculate(output, y)

predictions = np.argmax(output, axis=1)
if len(y.shape) == 2: class_targets = np.argmax(y, axis=1)
else: class_targets = y
accuracy = np.mean(predictions==class_targets)

print(f"loss = {loss}, accuracy = {accuracy:%}")