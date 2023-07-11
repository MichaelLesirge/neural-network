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
        self.biases = np.zeros(output_size, dtype=float)

        # save activation function
        self.activation = activation

    def forward(self, input: np.ndarray) -> np.ndarray:
        self.input = input

        # standard forward pass of neuron with no activation
        forward = np.dot(self.input, self.weights) + self.biases

        # use activation function
        return self.activation.func(forward)

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        
        # factor in gradient from activation function
        output_gradient = self.activation.gradient(output_gradient)

        # calculate gradient of input by linking up output_gradients with columns that align with that output
        input_gradient = np.dot(self.weights.T, output_gradient)

        # 
        weights_gradient = np.dot(output_gradient, self.input.T)
        # biases gradient stays output gradient
        biases_gradient = output_gradient

        # change 
        self.weights -= learning_rate * weights_gradient
        self.biases -= learning_rate * biases_gradient
        
        return input_gradient
    
def main():
    from activations import ReLU
    
    l = Dense(2, 3, activation=ReLU())
    
    l.weights = np.array([[3, 4, 5],
                          [6, 7, 8]])
    l.biases = np.array([9, 10, 11])
    
    # print(l.forward([1, 2]))
    print(l.forward([[1, 2], [1, 2]]))
    
if __name__ == "__main__":
    main()