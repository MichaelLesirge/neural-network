import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent.parent))

from activations import *
from matplotlib import pyplot as plt

def main():
    all = [BinaryStep(), Sigmoid(), HardSigmoid(), Tanh(), Affine(), Linear(), Exponential(), ReLU(), LeakyReLU(), ELU(), GELU(), SELU(), Swish(), Softplus(), Softmax()]
    common = [Sigmoid(), Tanh(), ReLU(), LeakyReLU(), ELU(), GELU(), Swish()]

    x= np.linspace(-1, 1, 100)

    for activation in common:
        y = activation.activation(x)
        m = activation.activation_prime(x)

        plt.title(repr(activation))
        plt.axhline(0, color='dimgrey', linewidth=1)
        plt.axvline(0, color='dimgrey', linewidth=1)

        plt.xlim(-1, 1)
        plt.ylim(-1, 1)

        plt.plot(x, m, label="activation prime", linestyle="--")
        plt.plot(x, y, label="activation")

        plt.legend(loc="best")
        plt.show()

if __name__ == "__main__":
    main()