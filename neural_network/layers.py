import numpy as np
from abc import ABC, abstractmethod

class Layer(ABC):
    _verbose_name = None
    
    def __str__(self) -> str:
        return f"<{(self._verbose_name if self._verbose_name is None else type(self).__name__).title()} {super(self).__name__.title()}>"

    def __repr__(self) -> str:
        dict_str = ", ".join(f"{key}={value}" for key, value in self.__dict__.items() if not key.startswith("_"))
        return f"{type(self).__name__}({dict_str})"
    
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def forward(inputs: np.ndarray) -> np.ndarray:
        ...
    
    @abstractmethod
    def backward(inputs: np.ndarray, output_gradient: np.ndarray, learning_rate: np.float64) -> np.ndarray:
        ...

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
    
class Softmax(Layer):
    """Put with layers since it needs output gradient"""
    _verbose_name = "softmax"

    def __init__(self):
        super().__init__()

    def activation(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / np.sum(e_x, axis=-1, keepdims=True)

    def backward(self, inputs, output_gradient):
        input_derivative = np.empty_like(output_gradient)
        output = self(inputs)
        
        for index, (single_output, single_grad) in enumerate(zip(output, output_gradient)):
            single_output = single_output.reshape(-1, 1)
            jacobian_matrix = np.diagflat(single_output) - np.dot(single_output, single_output.T)
            input_derivative[index] = np.dot(jacobian_matrix, single_grad)
            
        return input_derivative