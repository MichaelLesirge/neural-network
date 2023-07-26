import numpy as np
from activations import Activation
from abc import ABC, abstractmethod

# Activations network class has list of activations that each layer operates on. Activations are also layers.

class Layer(ABC):
    @abstractmethod
    def forward(self, input: np.ndarray) -> np.ndarray:
        ...

    @abstractmethod
    def backward(self, input: np.ndarray, output_gradient: np.ndarray, learning_rate: float):
        ...

class Dense(Layer):
    def __init__(self, input_size, output_size):
        self.weights = np.random.random((input_size, output_size))
        self.biases = np.zeros(output_size)

    def forward(self, input):
        return np.dot(input, self.weights) + self.biases

    def backward(self, input, output_gradient, learning_rate):
        weights_gradient = np.dot(output_gradient, input.T)
        
        input_gradient = np.dot(self.weights.T, output_gradient)
        
        self.weights -= learning_rate * weights_gradient
        self.biases -= learning_rate * output_gradient
        
        return input_gradient
    
def main():
    from activations import Sigmoid, ReLU

    l = Dense(2, 3, activation=ReLU())
    
    print(l.forward([1, 2]))
    print(l.forward([[1, 2], [1, 2]]))

    
if __name__ == "__main__":
    main()