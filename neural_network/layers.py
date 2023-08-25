from abc import ABC, abstractmethod

import numpy as np

from neural_network.base import BaseLayer


class Layer(BaseLayer, ABC):
    pass


# every class should only take how many outputs and then the next layer will use that for n_inputs when model.compile()
# class Reshape(Layer):
# class Flatten(Layer):
# class Input(Layer)

class Reshape(Layer):
    _verbose_name = "reshape"
    
    def __init__(self, in_shape, out_shape) -> None:
        super().__init__()
        self.in_shape = in_shape
        self.out_shape = out_shape

    def forward(self, inputs):
        return inputs.reshape(-1, *self.out_shape)
    
    def backward(self, inputs, output_gradient, learning_rate):
        return inputs * output_gradient.reshape(-1, *self.in_shape)

class Dense(Layer):
    _verbose_name = "fully connected layer"
    
    def __init__(self, n_inputs, n_outputs) -> None:
        self.weights = np.random.randn(n_inputs, n_outputs) * 0.01
        self.bias = np.zeros((1, n_outputs), dtype=float)

    def forward(self, inputs):
        return np.dot(inputs, self.weights) + self.bias

    def backward(self, inputs, output_gradient, learning_rate):
        weights_gradient = np.dot(inputs.T, output_gradient)

        bias_gradient = np.sum(output_gradient, axis=0, keepdims=True)

        input_gradient = np.dot(output_gradient, self.weights.T)
        
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * bias_gradient
        
        return input_gradient