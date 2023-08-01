from abc import ABC, abstractmethod

import numpy as np


class BaseLayer(ABC):
    _verbose_name = ""
    
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"<{type(self).__base__.__name__} {self._verbose_name if self._verbose_name else type(self).__name__}>".title()

    def __repr__(self) -> str:
        dict_str = ", ".join(f"{key}={value}" for key, value in self.__dict__.items() if not key.startswith("_"))
        return f"{type(self).__name__}({dict_str})"

    @abstractmethod
    def forward(self, inputs: np.ndarray) -> np.ndarray:
        pass
    
    @abstractmethod
    def backward(self, inputs: np.ndarray, output_gradient: np.ndarray, learning_rate: np.ndarray) -> np.ndarray:
        pass