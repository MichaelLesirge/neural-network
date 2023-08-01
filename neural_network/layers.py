from abc import ABC, abstractmethod

import numpy as np

from base import BaseLayer


class Layer(BaseLayer, ABC):
    pass


class Dense(Layer):
    def __init__(self, n_inputs, n_outputs) -> None:
        self.weights = np.random.randn(n_inputs, n_outputs)
        self.bias = np.zeros((1, n_outputs), dtype=float)

    def forward(self, inputs):
        return np.dot(inputs, self.weights) + self.bias

    def backward(self, inputs, output_gradient, learning_rate):
        weights_gradient = np.dot(inputs.T, output_gradient)

        bias_gradient = np.sum(output_gradient, axis=1, keepdims=True)

        input_gradient = np.dot(output_gradient, self.weights.T)
        
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * bias_gradient
        
        return input_gradient