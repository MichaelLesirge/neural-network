from abc import ABC, abstractmethod
import numpy as np

class Layer(ABC):
    _verbose_name = None
    
    def __str__(self) -> str:
        return f"<{(self._verbose_name if self._verbose_name is None else type(self).__name__).title()}>"

    def __repr__(self) -> str:
        dict_str = ", ".join(f"{key}={value}" for key, value in self.__dict__.items() if not key.startswith("_"))
        return f"{type(self).__name__}({dict_str})"
    
    @abstractmethod
    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """
        Forward for batch
        """
        ...

    @abstractmethod
    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        """Backward for batch"""
        ...
