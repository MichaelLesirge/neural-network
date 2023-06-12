import numpy as np
from abc import ABC, abstractmethod

# https://www.v7labs.com/blog/neural-networks-activation-functions


class ActivationBase(ABC):
    def __init__(self):
        self.__verbose_name = "Activation"
        super().__init__()

    def __str__(self) -> str:
        return f"<{self.__verbose_name}>"

    def __repr__(self) -> str:
        dict_str = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"{type(self).__name__}({dict_str})"

    @abstractmethod
    def func(self, x):
        ...

    @abstractmethod
    def gradient(self, x):
        ...


def binary_step(x, *, threshold=0):
    """
    Binary Step.
    Cons: Only works for binary outputs, bad for back prop because gradient is always 0.
    """
    return np.where(x < threshold, 0.0, 1.0)


def linear(x):
    """
    Linear / No Activation.
    Cons: All layers will just become basically one layer, bad for back prop because gradient is always 1.
    """
    return x


def sigmoid(x):
    """
    Sigmoid / Logistic Activation Function. Creates S shape between 0 and 1
    Good for models that predicting probability since it is between 0 and 1.
    Pros: Smooth gradient so no jumping around, always between 0 and 1.
    Cons: Little change in output from values ~3 or more from zero.
    """
    return 1 / (1 + np.exp(-x))


def hard_sigmoid(x):
    """
    Hard Sigmoid. Fast approximation of sigmoid
    """
    return np.clip(0.2 * x + 0.5, 0.0, 1.0)


def tanh(x):
    """
    Tanh Function (Hyperbolic Tangent).
    Similar to sigmoid, but between -1 and 1. It is usually used in hidden layers
    Pros: Zero centered so it can be seen as either negative, positive, or neutral;
    and it keeps the data centered making learning easier because gradients can move both positive or negative
    Cons: Same problem as sigmoid, little change in values ~3 or more from zero.
    """
    return np.tanh(x)


def relu(x):
    """
    Rectified Linear Unit.
    Relu does not activate all the neurons, only a subset, reducing needed calculations.
    Pros: Efficient because it sets negative values to 0 and leaves rest the same, this gives it linearity and non-saturation properties
    Cons: Can make "dead" neurons that don't have their weights and biases updated and that never get activated, also since it sets all negative to zero it loses some training data
    """
    return np.maximum(x, 0)


def leaky_relu(x):
    """
    Leaky Rectified Linear Unit.
    Pros: Same as relu but enables back prop even for negative values
    Cons: Time consuming to train with gradient decent due to small slope for negative values
    """
    return np.maximum(x, x * 0.01)


def elu(x, alpha=1):
    """
    Exponential Linear Units.
    Pros: Same as relu but is smooths softly, avoids dead neurons
    Cons: Increased computation time because of exp, no learning of alpha value, can have exploding gradient problem
    """
    return np.where(x >= 0, x, alpha * (np.exp(x) - 1))


def softmax(x):
    """
    Softmax.
    Good for output layer as it makes sum of 1
    """
    return np.exp(x) / np.sum(np.exp(x))


def swish(x):
    """
    Swish. 
    Pros: Does not abruptly change directions like ReLU, keeps small negatives that may be important but zeros out larger ones,  
    """
    return x * sigmoid(x)


def gelu(x):
    """
    Gaussian error linear unit
    """


def main() -> None:
    from matplotlib import pyplot as plt

    x_min, x_max = -2, 2
    y_min, y_max = -2, 2

    precision = 100

    x = np.array([i/precision for i in range(precision * x_min, precision * x_max + 1)], dtype=np.float64)

    activation_funcs = [linear, binary_step, sigmoid,
                        hard_sigmoid, tanh, relu, leaky_relu, elu, swish]
    # activation_funcs = [linear, binary_step]
    # activation_funcs = [sigmoid, tanh]
    # activation_funcs = [sigmoid, hard_sigmoid]
    # activation_funcs = [relu, leaky_relu, elu]
    # activation_funcs = [swish, gelu]

    plt.ylim(y_min, y_max)

    # test_times(activation_funcs)

    for func in activation_funcs:
        y = func(x)
        plt.plot(x, y, label=(func.pyfunc if isinstance(func, np.vectorize) else func).__name__)

    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    main()
