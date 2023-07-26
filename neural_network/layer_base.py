from abc import ABC, abstractmethod
import numpy as np


class Layer(ABC):
    @abstractmethod
    def forward(self, inputs: np.ndarray) -> np.ndarray:
        ...

    @abstractmethod
    def backward(self, inputs: np.ndarray, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        ...
