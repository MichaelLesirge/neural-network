import numpy as np
from nnfs.datasets import vertical_data, spiral_data
from matplotlib import pyplot as plt

# Sorry for crappy code, just doing it to get my head around it
# https://www.youtube.com/playlist?list=PLQVvvaa0QuDcjD5BAw2DxE6OF2tius3V3. Ended on ep9, no ep10 :(

class LayerDense:
    def __init__(self, n_inputs: int, n_neurons: int) -> None:
        
        self.weights = np.random.rand(n_inputs, n_neurons) - 0.5
        
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        output = np.dot(inputs, self.weights) + self.biases
        return output

class ActivationReLU:
    def forward(self, inputs: np.ndarray) -> np.ndarray:
        return np.maximum(inputs, 0)

class ActivationSoftMax:
    def forward(self, x: np.ndarray) -> np.ndarray:
        exp_x = np.exp(x - x.max(axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

class LossCategoricalCrossEntropy:
    def calculate(self, output: np.ndarray, y: np.ndarray) -> float:                
        return np.mean(self.forward(output, y))
    
    def forward(self, y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        
        if len(y_true.shape) == 1:
            y_pred = np.eye[len(y_pred), y_true]
        elif len(y_true.shape) == 2:
            y_pred = np.sum(y_pred * y_true, axis=1)
            
        y_pred = np.clip(y_pred, 1e-7, 1-1e-7)
        negative_log_likelihoods = -np.log(y_pred)
        
        return negative_log_likelihoods 
        

X, y_true = vertical_data(samples=100, classes=3)

dense1 = LayerDense(2,5)
dense2 = LayerDense(5,5)
dense3 = LayerDense(5,3)

relu_function = ActivationReLU()
softmax_function = ActivationSoftMax()

loss_function = LossCategoricalCrossEntropy()

pred = dense1.forward(X)
pred = relu_function.forward(pred)
pred = dense2.forward(pred)
pred = relu_function.forward(pred)
pred = dense3.forward(pred)
pred = softmax_function.forward(pred)

loss = loss_function.calculate(pred, y_true)

print(loss)

prediction = np.argmax(pred, axis=1)
accuracy = np.mean(prediction == y_true)

# print(format(accuracy, "%"))
# plt.scatter(X[:, 0], X[:, 1], c=y_true, s=40, cmap="brg")
# plt.show()