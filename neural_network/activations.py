import numpy as np
from abc import ABC, abstractmethod


class Activation(ABC):
    _verbose_name = "activation"

    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return f"<{self._verbose_name.title()}>"

    def __repr__(self) -> str:
        dict_str = ", ".join(f"{key}={value}" for key,
                             value in self.__dict__.items() if not key.startswith("_"))
        return f"{type(self).__name__}({dict_str})"

    def __call__(self, z: np.ndarray) -> np.ndarray:
        return self.func(z)

    @abstractmethod
    def func(self, inputs: np.ndarray) -> np.ndarray:
        ...

    @abstractmethod
    def gradient(self, output_gradient: np.ndarray) -> np.ndarray:
        ...

# https://www.v7labs.com/blog/neural-networks-activation-functions


class BinaryStep(Activation):
    """ 
    Binary Step.
    Cons: Only works for binary outputs, bad for back prop because gradient is always 0.
    """
    _verbose_name = "binary step"

    def __init__(self, threshold=0.0):
        super().__init__()
        self.threshold = threshold

    def func(self, inputs):
        return np.where(inputs < self.threshold, 0.0, 1.0)

    def gradient(self, output_gradient):
        return np.zeros_like(output_gradient, dtype=float)


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

    def func(self, inputs):
        return 1.0 / (1.0 + np.exp(-inputs))

    def gradient(self, output_gradient):
        s = self.func(output_gradient)
        return s * (1.0-s)


class HardSigmoid(Activation):
    """
    Hard Sigmoid.
    Fast approximation of sigmoid.
    """
    _verbose_name = "hard sigmoid"

    def __init__(self):
        super().__init__()

    def func(self, inputs):
        inputs = 0.2 * inputs + 0.5
        return np.clip(inputs, 0.0, 1.0)

    def gradient(self, output_gradient):
        return np.where((output_gradient >= -2.5) & (output_gradient <= 2.5), 0.2, 0.0)


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

    def func(self, inputs):
        return np.tanh(inputs)

    def gradient(self, output_gradient):
        return 1 - np.tanh(output_gradient) ** 2


class Affine(Activation):
    """
    Affine.
    Just y = mx + b
    """
    _verbose_name = "Affine"

    def __init__(self, slope=1, intercept=0):
        super().__init__()
        self.slope = slope
        self.intercept = intercept

    def func(self, inputs):
        return self.slope * inputs + self.intercept

    def gradient(self, output_gradient):
        return np.ones_like(output_gradient, dtype=float) * self.slope


class Linear(Affine):
    """ 
    Linear / Identity / No activation.
    Cons: All layers will just become basically one layer, bad for back prop because gradient is always 1.
    """
    _verbose_name = "linear"

    def __init__(self):
        super().__init__(slope=1, intercept=0)
        
class Exponential(Activation):
    _verbose_name = "Exponential"
    
    def __init__(self):
        super().__init__()

    def func(self, inputs):
        return np.exp(inputs)

    def gradient(self, output_gradient):
        return np.exp(output_gradient)

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

    def func(self, inputs):
        return np.maximum(inputs, 0.0)

    def gradient(self, output_gradient):
        return (output_gradient > 0).astype(float)


class LeakyReLU(Activation):
    """
    Leaky Rectified Linear Unit.
    Pros: Same as relu but enables back prop even for negative values
    Cons: Time consuming to train with gradient decent due to small slope for negative values
    """
    _verbose_name = "leaky rectified linear unit"

    def __init__(self, alpha=0.3):
        super().__init__()
        self.alpha = alpha

    def func(self, inputs):
        return np.where(inputs > 0, inputs, inputs * self.alpha)

    def gradient(self, output_gradient):
        return np.where(output_gradient > 0, 1.0, self.alpha)


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

    def func(self, inputs):
        return np.where(inputs > 0, inputs, self.alpha * (np.exp(inputs) - 1))

    def gradient(self, output_gradient):
        np.where(output_gradient > 0, 1.0,
                 self.alpha * np.exp(output_gradient))


# Todo: GELU (gaussian Error Linear Unit), SELU (scaled exponential linear unit), and SoftPlus


class Softmax(Activation):
    """
    Softmax.
    Good for output layer as it makes sum of 1.
    """
    _verbose_name = "softmax"

    def __init__(self):
        super().__init__()

    def func(self, inputs):
        e_x = np.exp(inputs - np.max(inputs, axis=-1, keepdims=True))
        self._output = e_x / np.sum(e_x, axis=-1, keepdims=True)
        return self._output

    def _gradient(self, output_gradient, last_output):
        return np.dot((np.identity(np.size(output_gradient), dtype=float) - last_output.T) * last_output, output_gradient)

    def gradient(self, output_gradient):
        # n = np.size(output_gradient, axis=-1)
        # return np.dot((np.identity(n, dtype=float) - self.output.T) * self.output, output_gradient)

        is_batch = len(output_gradient.shape) == 2

        if is_batch:
            return np.array([self._gradient(grad, out) for grad, out in zip(output_gradient, self._output)])
        else:
            return self._gradient(output_gradient, self._output)


def main() -> None:

    def binary_cross_entropy(y_true, y_pred):
        return np.mean((-y_true * np.log(y_pred)) - (1 - y_true) * np.log(1 - y_pred))

    def binary_cross_entropy_prime(y_true, y_pred):
        return (((1 - y_true) / (1 - y_pred)) - (y_true / y_pred)) / np.size(y_true, axis=-1)

    y_pred = np.array(
        [[0.4, 0.7, 0.2, 1.3], [0.4, 0.7, 0.2, 1.3]], dtype=float)
    y_true = np.array(
        [[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]], dtype=float)
    # y_pred = np.array([0.4, 0.7, 0.2, 1.3], dtype=float)
    # y_true = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    print(y_pred)
    print(y_true)

    softmax = Softmax()

    y_pred = softmax(y_pred)
    print()
    print(y_pred)

    gradient = binary_cross_entropy_prime(y_true, y_pred)
    print()
    print(gradient)

    gradient = softmax.gradient(gradient)
    print()

    # --- Plots ---
    from matplotlib import pyplot as plt

    x_min, x_max = -5, 5

    precision = 100

    x = np.array([i/precision for i in range(precision * x_min,
                 precision * x_max + 1)], dtype=np.float64)

    activation_funcs = [Linear(), BinaryStep(), Sigmoid(),
                        HardSigmoid(), Tanh(), ReLU(), LeakyReLU(), ELU(), Swish()]

    for activation in activation_funcs:
        y = activation(x)

        plt.title(str(activation))
        plt.plot(x, y, label="func")
        plt.plot(x, activation.gradient(y), label="grad")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    main()
