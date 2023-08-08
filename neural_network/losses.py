from abc import ABC, abstractmethod

import numpy as np

from base import BaseLayer


class Loss(BaseLayer, ABC):
    def __init__(self) -> None:
        super().__init__()
 
    def forward(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        
        if y_true.ndim == 1:
            classes = np.size(y_pred, 1)
            y_true = np.eye(classes)[range(classes), y_true]
        
        loss = self.loss(y_true, y_pred)
        return np.mean(loss)
    
    def backward(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        samples = np.size(y_true, 0)
    
    @abstractmethod
    def loss(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        pass
        
    def loss_prime(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        pass