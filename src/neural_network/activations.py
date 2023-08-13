from abc import ABC, abstractmethod

import numpy as np

from neural_network.base import BaseLayer


class Activation(BaseLayer, ABC):
    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.activation(x)

    def __init__(self) -> None:
        super().__init__()

    def forward(self, inputs):
        return self.activation(inputs)

    def backward(self, inputs, output_gradient, learning_rate=None):
        return output_gradient * self.activation_prime(inputs)

    @abstractmethod
    def activation(self, x: np.ndarray) -> np.ndarray:
        ...

    @abstractmethod
    def activation_prime(self, x: np.ndarray) -> np.ndarray:
        ...


class BinaryStep(Activation):
    """ 
    Binary Step.
    Cons: Only works for binary outputs, bad for back prop because gradient is always 0.
    """
    _verbose_name = "binary step"

    def __init__(self, threshold=0.0):
        super().__init__()
        self.threshold = threshold

    def activation(self, x):
        return np.where(x < self.threshold, 0.0, 1.0)

    def activation_prime(self, x):
        return np.zeros_like(x, dtype=float)


class Sigmoid(Activation):
    """
    Sigmoid / Logistic Activation Function.
    Creates S shape between 0 and 1.
    Good for models that predicting probability since it is between 0 and 1.
    Pros: Smooth gradient so no jumping around, always between 0 and 1.
    Cons: Little change in output from values ~3 or more from zero.
    """
    _verbose_name = "logistic activation function"

    def __init__(self):
        super().__init__()

    def activation(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def activation_prime(self, output_gradient):
        s = self(output_gradient)
        return s * (1.0-s)


class HardSigmoid(Activation):
    """
    Hard Sigmoid.
    Fast approximation of sigmoid.
    """
    _verbose_name = "hard sigmoid"

    def __init__(self):
        super().__init__()

    def activation(self, x):
        x = 0.2 * x + 0.5
        return np.clip(x, 0.0, 1.0)

    def activation_prime(self, x):
        return np.where((x >= -2.5) & (x <= 2.5), 0.2, 0.0)


class Tanh(Activation):
    """
    Tanh / Hyperbolic Tangent.
    Similar to sigmoid, but between -1 and 1. It is usually used in hidden layers
    Pros: Zero centered so it can be seen as either negative, positive, or neutral;
    and it keeps the data centered making learning easier because gradients can move both positive or negative
    Cons: Same problem as sigmoid, little change in values ~3 or more from zero.
    """
    _verbose_name = "hyperbolic tangent"

    def __init__(self):
        super().__init__()

    def activation(self, x):
        return np.tanh(x)

    def activation_prime(self, x):
        return 1 - np.tanh(x) ** 2


class Affine(Activation):
    """
    Affine.
    Just y = mx + b
    """
    _verbose_name = "affine"

    def __init__(self, slope=1, intercept=0):
        super().__init__()
        self.slope = slope
        self.intercept = intercept

    def activation(self, x):
        return self.slope * x + self.intercept

    def activation_prime(self, x):
        return np.ones_like(x, dtype=float) * self.slope


class Linear(Activation):
    """ 
    Linear / Identity / No activation.
    Cons: All layers will just become basically one layer, bad for back prop because gradient is always 1.
    """
    _verbose_name = "linear"

    def __init__(self):
        super().__init__()

    def activation(self, x):
        return x

    def activation_prime(self, x):
        return np.ones_like(x, dtype=float)


class Exponential(Activation):
    _verbose_name = "Exponential"

    def __init__(self):
        super().__init__()

    def activation(self, x):
        return np.exp(x)

    def activation_prime(self, x):
        return np.exp(x)


class ReLU(Activation):
    """
    Rectified Linear Unit.
    Relu does not activate all the neurons, only a subset, reducing needed calculations.
    Pros: Efficient because it sets negative values to 0 and leaves rest the same, this gives it linearity and non-saturation properties
    Cons: Can make "dead" neurons that don't have their weights and biases updated and that never get activated, also since it sets all negative to zero it loses some training data
    """
    _verbose_name = "rectified linear unit"

    def __init__(self):
        super().__init__()

    def activation(self, x):
        return np.maximum(x, 0.0)

    def activation_prime(self, x):
        return (x > 0).astype(float)


class LeakyReLU(Activation):
    """
    Leaky Rectified Linear Unit.
    Pros: Same as relu but enables back prop even for negative values
    Cons: Time consuming to train with gradient decent due to small slope for negative values
    """
    _verbose_name = "leaky rectified linear unit"

    def __init__(self, alpha=0.1):
        super().__init__()
        self.alpha = alpha

    def activation(self, x):
        return np.where(x > 0, x, x * self.alpha)

    def activation_prime(self, x):
        return np.where(x > 0, 1.0, self.alpha)


class ELU(Activation):
    """
    Exponential Linear Units.
    Pros: Same as relu but is smooths softly, avoids dead neurons
    Cons: Increased computation time because of exp, no learning of alpha value, can have exploding gradient problem
    """
    _verbose_name = "exponential linear units"

    def __init__(self, alpha=1):
        super().__init__()
        self.alpha = alpha

    def activation(self, x):
        return np.where(x > 0, x, self.alpha * (np.exp(x) - 1))

    def activation_prime(self, x):
        return np.where(x > 0, 1.0, self.alpha * np.exp(x))


class GELU(Activation):
    """
    Approximate Gaussian Error Linear Unit.

    Pros: Like ReLU, buts weights inputs by their value instead of sign
    """
    _verbose_name = "approximate gaussian error linear unit"

    def __init__(self):
        super().__init__()
        # self.approximate = approximate

    def activation(self, x):
        return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))

    def activation_prime(self, x):
        erf_prime = (2 / np.sqrt(np.pi)) * np.exp(-((x / np.sqrt(2)) ** 2))
        approx = np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3))
        return 0.5 + (0.5 * approx) + ((0.5 * x * erf_prime) / np.sqrt(2))


class SELU(Activation):
    """
    Scaled Exponential Linear Unit.

    Pros: Can be good when used with correct weight initialization and regularization 
    Cons: Need special initialization and regularization 
    """
    _verbose_name = "scaled exponential linear unit"

    def __init__(self):
        super().__init__()
        self.alpha = 1.6732632423543772848170429916717
        self.scale = 1.0507009873554804934193349852946
        self._elu = ELU(alpha=self.alpha)

    def activation(self, x):
        return self.scale * self._elu(x)

    def activation_prime(self, x):
        return self.scale * np.where(x >= 0, 1.0, np.exp(x) * self.alpha)


class Swish(Activation):
    """
    Swish.
    Pros: smoother curve then ReLU, large negative numbers are zeroed out while smaller ones are kept
    """
    _verbose_name = "swish"

    def __init__(self):
        super().__init__()
        # self.beta = beta
        self._sigmoid = Sigmoid()

    def activation(self, x):
        return x * self._sigmoid(x)

    def activation_prime(self, x):
        return x * self._sigmoid.activation_prime(x) + self._sigmoid(x)


class Softplus(Activation):
    """
    Softplus.

    Output is always positive
    Pros: Like a smooth ReLU
    Cons: Slowish to compute compared to ReLU
    """
    _verbose_name = "softplus"

    def __init__(self):
        super().__init__()

    def activation(self, x):
        return np.log(np.exp(x) + 1)

    def activation_prime(self, x):
        exp_x = np.exp(x)
        return exp_x / (exp_x + 1)


class Softmax(Activation):
    """
    Softmax.
    Good for output layer as it makes sum of 1.
    """
    _verbose_name = "softmax"

    def __init__(self):
        super().__init__()

    def activation(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / np.sum(e_x, axis=-1, keepdims=True)

    def backward(self, inputs, output_gradient, learning_rate=None):
        # Create uninitialized array
        input_derivative = np.empty_like(output_gradient)
        output = self(inputs)

        # Enumerate outputs and gradients
        for index, (single_output, single_grad) in enumerate(zip(output, output_gradient)):
            single_output = single_output.reshape(-1, 1)
            jacobian_matrix = np.diagflat(single_output) - np.dot(single_output, single_output.T)
            input_derivative[index] = np.dot(jacobian_matrix, single_grad)

        return input_derivative

    def activation_prime(self, x, output_gradient):
        return self.backward(x, output_gradient)


__all__ = [BinaryStep, Sigmoid, HardSigmoid, Tanh, Affine, Linear,
           Exponential, ReLU, LeakyReLU, ELU, GELU, SELU, Swish, Softplus, Softmax]

def main() -> None:
    from matplotlib import pyplot as plt

    x_min, x_max = -5, 5

    precision = 100

    x = np.array([i/precision for i in range(precision * x_min,precision * x_max + 1)], dtype=np.float64)

    x = x.reshape(x.shape + (1,))

    activation_funcs: list[Activation] = [
        activation() for activation in __all__ if activation not in [Softmax]]

    for activation in activation_funcs:
        y = activation(x)

        plt.title(repr(activation))
        plt.axhline(0, color='dimgrey', linewidth=1)
        plt.axvline(0, color='dimgrey', linewidth=1)
        # plt.ylim(-1.2, 1.2)

        plt.plot(x, y, label="activation")
        plt.plot(x, activation.activation_prime(x), label="activation prime")

        print(activation)

        plt.legend(loc="best")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    main()
