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
    def __init__(self, input_size, output_size, activation):
        self.weights = np.random.randn(output_size, input_size)
        self.biases = np.ones((output_size, 1))

        self.activation = activation

    def forward(self, input):
        self.input = input
        return np.dot(self.weights, self.input) + self.biases

    def backward(self, output_gradient, learning_rate):
        weights_gradient = np.dot(output_gradient, self.input.T)
        
        input_gradient = np.dot(self.weights.T, output_gradient)
        
        self.weights -= learning_rate * weights_gradient
        self.biases -= learning_rate * output_gradient
        
        return input_gradient
    
def main():
    from activations import Sigmoid, ReLU

    l = Dense(2, 3, activation=ReLU())
    
    # l.weights = np.array([[3, 4, 5],
    #                       [6, 7, 8]])
    # l.biases = np.array([9, 10, 11])
    
    print(l.forward([[1], [2]]))
    print(l.forward([[[1], [2]], [[1], [2]]]))
    
if __name__ == "__main__":
    main()