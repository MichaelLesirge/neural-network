from abc import ABC, abstractmethod

import numpy as np

class Layer(ABC):
    def __str__(self) -> str:
        return f"<{(self._verbose_name or __class__.__name__).title()} {self.__class__.__base__.__name__.title()}>"

    def __repr__(self) -> str:
        dict_str = ", ".join(f"{key}={value}" for key, value in self.__dict__.items() if not key.startswith("_"))
        return f"{type(self).__name__}({dict_str})"

    def forward(self, inputs: np.ndarray) -> np.ndarray: pass
    def backward(self, inputs: np.ndarray, output_gradient: np.ndarray, learning_rate: np.ndarray) -> np.ndarray: pass

class Dense(Layer):
    _verbose_name = "fully connected"
    
    def __init__(self, n_neurons: int, activation):
        self._is_initialized = False
        
        self.input_size = None
        self.output_size = n_neurons
        self.activation = activation
    
    def _init_params(self):
        self.weights = np.random.randn(self.input_size, self.output_size)
        self.biases = np.zeros((1, self.output_size), dtype=np.float64)

        self._is_initialized = True

    def forward(self, inputs):
        if not self._is_initialized:
            self.n_in = np.size(inputs, axis=-1)
            self._init_params()
        
        return np.dot(inputs, self.weights) + self.biases

    def backward(self, inputs, output_gradient, learning_rate):
        weights_gradient = np.dot(inputs.T, output_gradient)
        bias_gradient = np.sum(output_gradient, axis=0, keepdims=True)
        
        input_gradient = np.dot(self.weights.T, output_gradient)
        
        self.weights -= learning_rate * weights_gradient
        self.biases -= learning_rate * bias_gradient
        
        return input_gradient 