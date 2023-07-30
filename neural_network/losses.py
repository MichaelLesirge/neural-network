from abc import ABC, abstractmethod

import numpy as np


class Loss(ABC):
    _verbose_name = ""
    
    def __str__(self) -> str:
        return f"<{(self._verbose_name or __class__.__name__).title()} Loss>"

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    @abstractmethod
    def loss(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.float64: pass
    
    @abstractmethod
    def gradient(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray: pass

class MSE(Loss):
    _verbose_name = "mean squared error"
    
    def loss(self, y_true, y_pred) :
        return np.mean(np.square(y_true - y_pred))

    def gradient(self, y_true, y_pred):
        return 2 * (y_pred - y_true) / np.size(y_pred, axis=-1)

class BinaryCrossentropy(Loss):
    _verbose_name = "binary crossentropy"
    
    def loss(self, y_true, y_pred):
        return np.mean((-y_true * np.log(y_pred)) - (1 - y_true) * np.log(1 - y_pred))

    def gradient(y_true, y_pred):
        return (((1 - y_true) / (1 - y_pred)) - (y_true / y_pred)) / np.size(y_true, axis=-1)
    
class CategoricalCrossentropy(Loss):
    _verbose_name = "categorical crossentropy"
    
    def loss(self, y_true, y_pred):
        return y_true
    
    def gradient(y_true, y_pred):
        pass