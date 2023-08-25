from abc import ABC, abstractmethod

import numpy as np

from neural_network.base import BaseLayer


class Loss(BaseLayer, ABC):
    def __init__(self, categorical_labels: bool = None) -> None:
        super().__init__()
        self.categorical_labels = categorical_labels
 
    def _labels_to_one_hot(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        classes = np.size(y_pred, 1)
        y_true = np.eye(classes)[y_true]
        return y_true
    
    def forward(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        if self.categorical_labels or (self.categorical_labels is None and y_true.ndim == 1):
            y_true = self._labels_to_one_hot(y_true, y_pred)
        
        loss = self.loss(y_true, y_pred)
        return np.mean(loss)
    
    def backward(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        if self.categorical_labels or (self.categorical_labels is None and y_true.ndim == 1):
            y_true = self._labels_to_one_hot(y_true, y_pred)
            
        samples = np.size(y_true, 0)
        loss_prime = self.loss_prime(y_true, y_pred)
        
        return loss_prime / samples
    
    @abstractmethod
    def loss(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        pass
        
    def loss_prime(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        pass
    
class MSE(Loss):
    _verbose_name = "mean squared error"
    
    def __init__(self) -> None:
        super().__init__()
    
    def loss(self, y_true, y_pred):
        return np.square(y_true - y_pred)
    
    def loss_prime(self, y_true, y_pred):
        return 2 * (y_pred - y_true)
    
class BinaryCrossEntropy(Loss):
    _verbose_name = "binary cross entropy"
    
    def __init__(self, categorical_labels: bool = None) -> None:
        super().__init__(categorical_labels)
    
    def loss(self, y_true, y_pred):
        return -((y_true * np.log(y_pred)) + ((1 - y_true) * np.log(1 - y_pred)))
    
    def loss_prime(self, y_true, y_pred):
        return (1 - y_true) / (1 - y_pred) - y_true / y_pred
    
class CategoricalCrossEntropy(Loss):
    _verbose_name = "Categorical cross entropy"
    
    def __init__(self, categorical_labels: bool = None) -> None:
        super().__init__(categorical_labels)
    
    def loss(self, y_true, y_pred):
        y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
        return -np.log(np.sum(y_pred * y_true, axis=1))
         
    
    def loss_prime(self, y_true, y_pred):
        y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
        return -y_true / y_pred