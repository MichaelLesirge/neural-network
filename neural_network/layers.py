import numpy as np
from activations import Activation
from abc import ABC, abstractmethod

class Layer(ABC):
    @abstractmethod
    def forward(self, input: np.ndarray) -> np.ndarray:
        ...

    @abstractmethod
    def backward(self, output_gradient: np.ndarray, learning_rate: float):
        ...

class Dense(Layer):
    def __init__(self, input_size: int, output_size: int, activation: Activation) -> None:

        # Initialize weights from standard normal distribution.
        # Each row of weights lines up with a input and each column lines up with a output
        self.weights = np.random.randn(output_size, input_size)

        # Initialize biases to 0s.
        # One bias for each output.
        self.biases = np.zeros(output_size)

        # save activation function
        self.activation = activation

    def forward(self, input: np.ndarray) -> np.ndarray:
        self.input = input

        # standard forward pass of neuron
        forward = np.dot(self.weights, self.input) + self.biases

        # use activation function
        return self.activation.func(forward)

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        
        # factor in gradient from activation function
        output_gradient = self.activation.gradient(output_gradient)

        # calculate gradients
        input_gradient = np.dot(self.weights.T, output_gradient)

        weights_gradient = np.dot(output_gradient, self.input.T)
        biases_gradient = output_gradient

        # change 
        self.weights -= learning_rate * weights_gradient
        self.biases -= learning_rate * biases_gradient
        
        return input_gradient