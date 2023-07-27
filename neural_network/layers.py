import numpy as np
from base import Layer

class Dense(Layer):
    _verbose_name = "fully connected"
    
    def __init__(self, n_neurons: int):
        self._is_initialized = False
        
        self.input_size = None
        self.output_size = n_neurons
    
    def _init_params(self):
        self.weights = np.random.randn(self.input_size, self.output_size)
        self.biases = np.zeros((1, self.output_size), dtype=np.float64)

        self._is_initialized = True

    def forward(self, input):
        if not self._is_initialized:
            self.n_in = input.shape[1]
            self._init_params()
        
        return np.dot(input, self.weights) + self.biases

    def backward(self, input, output_gradient, learning_rate):
        weights_gradient = np.dot(output_gradient, input.T)
        
        input_gradient = np.dot(self.weights.T, output_gradient)
        
        self.weights -= learning_rate * weights_gradient
        self.biases -= learning_rate * output_gradient
        
        return input_gradient
