import numpy as np
from abc import ABC, abstractmethod

class Activation(ABC):
    _verbose_name = "activation"
    
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return f"<{self._verbose_name.title()}>"

    def __repr__(self) -> str:
        dict_str = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"{type(self).__name__}({dict_str})"
    
    def __call__(self, x):
        return self.func(x)

    @abstractmethod
    def func(self, x):
        ...

    @abstractmethod
    def gradient(self, x):
        ...

# https://www.v7labs.com/blog/neural-networks-activation-functions

class BinaryStep(Activation):
    _verbose_name = "binary step"

    def __init__(self, threshold=0):
        self.threshold = threshold
        super().__init__()

    def func(self, x):
        """ 
        Cons: Only works for binary outputs, bad for back prop because gradient is always 0.
        """
        return np.where(x < self.threshold, 0.0, 1.0)

    def gradient(self, x):
        pass


class Linear(Activation):
    _verbose_name = "linear"

    def __init__(self):
        super().__init__()

    def func(self, x):
        """ 
        No activation.
        Cons: All layers will just become basically one layer, bad for back prop because gradient is always 1.
        """
        return x

    def gradient(self, x):
        pass


class Sigmoid(Activation): 
    _verbose_name = "logistic activation function"

    def __init__(self):
        super().__init__()

    def func(self, x):
        """
        Sigmoid / Logistic Activation Function. Creates S shape between 0 and 1
        Good for models that predicting probability since it is between 0 and 1.
        Pros: Smooth gradient so no jumping around, always between 0 and 1.
        Cons: Little change in output from values ~3 or more from zero.
        """
        return 1 / (1 + np.exp(-x))

    def gradient(self, x):
        pass


class HardSigmoid(Activation): 
    _verbose_name = "hard sigmoid"

    def __init__(self):
        super().__init__()

    def func(self, x):
        """
        Hard Sigmoid. Fast approximation of sigmoid
        """
        return np.clip(0.2 * x + 0.5, 0.0, 1.0)

    def gradient(self, x):
        pass


class Tanh(Activation): 
    _verbose_name = "tanh"

    def __init__(self):
        super().__init__()

    def func(self, x):
        """
        Tanh Function (Hyperbolic Tangent).
        Similar to sigmoid, but between -1 and 1. It is usually used in hidden layers
        Pros: Zero centered so it can be seen as either negative, positive, or neutral;
        and it keeps the data centered making learning easier because gradients can move both positive or negative
        Cons: Same problem as sigmoid, little change in values ~3 or more from zero.
        """
        return np.tanh(x)

    def gradient(self, x):
        pass


class ReLU(Activation): 
    _verbose_name = "rectified linear unit"

    def __init__(self):
        super().__init__()

    def func(self, x):
        """
        Rectified Linear Unit.
        Relu does not activate all the neurons, only a subset, reducing needed calculations.
        Pros: Efficient because it sets negative values to 0 and leaves rest the same, this gives it linearity and non-saturation properties
        Cons: Can make "dead" neurons that don't have their weights and biases updated and that never get activated, also since it sets all negative to zero it loses some training data
        """
        return np.maximum(x, 0)

    def gradient(self, x):
        pass


class LeakyReLU(Activation): 
    _verbose_name = "leaky rectified linear unit"

    def __init__(self):
        super().__init__()

    def func(self, x):
        """
        Leaky Rectified Linear Unit.
        Pros: Same as relu but enables back prop even for negative values
        Cons: Time consuming to train with gradient decent due to small slope for negative values
        """
        return np.maximum(x, x * 0.01)

    def gradient(self, x):
        pass


class ELU(Activation): 
    _verbose_name = "exponential linear units"

    def __init__(self, alpha=1):
        self.alpha = alpha
        super().__init__()

    def func(self, x):
        """
        Exponential Linear Units.
        Pros: Same as relu but is smooths softly, avoids dead neurons
        Cons: Increased computation time because of exp, no learning of alpha value, can have exploding gradient problem
        """
        return np.where(x >= 0, x, self.alpha * (np.exp(x) - 1))

    def gradient(self, x):
        pass


class Softmax(Activation): 
    _verbose_name = "softmax"

    def __init__(self):
        super().__init__()

    def func(self, x):
        """
        Softmax.
        Good for output layer as it makes sum of 1
        """
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def gradient(self, x):
        pass


class Swish(Activation): 
    _verbose_name = "swish"

    def __init__(self):
        self.sigmoid = Sigmoid()
        super().__init__()

    def func(self, x):
        """
        Swish. 
        Pros: Does not abruptly change directions like ReLU, keeps small negatives that may be important but zeros out larger ones,  
        """
        return x * self.sigmoid(x)

    def gradient(self, x):
        pass

class GELU():
    _verbose_name = "Gaussian error linear unit"
    pass

def main() -> None:
    from matplotlib import pyplot as plt

    x_min, x_max = -2, 2
    y_min, y_max = -2, 2

    precision = 100

    x = np.array([i/precision for i in range(precision * x_min, precision * x_max + 1)], dtype=np.float64)

    activation_funcs = [Linear(), BinaryStep(), Sigmoid(),
                        HardSigmoid(), Tanh(), ReLU(), LeakyReLU(), ELU(), Swish()]

    plt.ylim(y_min, y_max)

    # test_times(activation_funcs)

    for func in activation_funcs:
        y = func(x)
        plt.plot(x, y, label = str(func))

    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    main()
