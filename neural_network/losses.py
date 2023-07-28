from abc import ABC, abstractmethod

import numpy as np


class Loss(ABC):
    _verbose_name = None
    
    def __str__(self) -> str:
        return f"<{(self._verbose_name if self._verbose_name is None else type(self).__name__).title()} {super(self).__name__}>"

    def __repr__(self) -> str:
        dict_str = ", ".join(f"{key}={value}" for key, value in self.__dict__.items() if not key.startswith("_"))
        return f"{type(self).__name__}({dict_str})"

    @abstractmethod
    def loss(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
        pass
    
    @abstractmethod
    def loss_prime(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        pass

class MSE(Loss):
    _verbose_name = "mean squared error"
    
    def loss(self, y_true, y_pred) :
        return np.mean(np.square(y_true - y_pred))

    def loss_prime(self, y_true, y_pred):
        return 2 * (y_pred - y_true) / np.size(y_pred, axis=-1)

class BinaryCrossentropy(Loss):
    _verbose_name = "binary crossentropy"
    
    def loss(self, y_true, y_pred):
        return np.mean((-y_true * np.log(y_pred)) - (1 - y_true) * np.log(1 - y_pred))

    def loss_prime(y_true, y_pred):
        return (((1 - y_true) / (1 - y_pred)) - (y_true / y_pred)) / np.size(y_true, axis=-1)
    
class CategoricalCrossentropy(Loss):
    _verbose_name = "categorical crossentropy"
    
    def loss(self, y_true, y_pred):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)

        # Probabilities for target values -
        # only if categorical labels
        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[
                range(samples),
                y_true
            ]
        # Mask values - only for one-hot encoded labels
        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(
                y_pred_clipped * y_true,
                axis=1
            )

        # Losses
        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods

    def loss_prime(y_true, y_pred):
