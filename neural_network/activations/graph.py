from activations import *
from matplotlib import pyplot as plt


def graph_all(x: np.ndarray = None) -> None:
    funcs: list[Activation] = [BinaryStep, Sigmoid, HardSigmoid, Tanh, Affine, Linear,
                               Exponential, ReLU, LeakyReLU, ELU, GELU, SELU, Swish, Softplus, Softmax]

    for activation in funcs:
        graph_activation(activation, x)


def graph_activation(activation: Activation, x: np.ndarray = None):

    if x is None:
        x = np.arange(-5, 5, 0.01)

    if x.ndim == 1:
        x = x.reshape((1, ) + x.shape)

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
