import numpy as np

from neural_network.losses import Loss
from neural_network.base import BaseLayer

# at some point add compile step where optimizations could be made and Dense Layers could find how many inputs they have  

def n_split_array(arr, n_size, *, keep_extra=True):
    """split arr into chunks of size n with extra added on end if keep_extra is true"""
    if n_size is None: return arr
    div, extra = divmod(np.size(arr, 0), n_size)
    a, b = np.split(arr, [extra]) if extra else arr, None
    return np.array_split(a, div) + ([b] if (b and keep_extra) else [])


def same_shuffle(*arrays):
    """shuffle 2 arrays """
    order = np.arange(np.size(arrays[0], 0))
    np.random.shuffle(order)
    return tuple(array[order] for array in arrays)

class Network:
    def __init__(self, layers: list[BaseLayer], loss: Loss) -> None:
        self.layers = layers
        self.loss = loss
    
    def compute(self, inputs: np.ndarray) -> np.ndarray:
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs
    
    
    def train(self, x: np.ndarray, y: np.ndarray, learning_rate: float = 0.001, batch_size: int = 32, epochs: int = 1, shuffle: bool = True, is_categorical_labels: bool = False):
        for epoch in range(epochs):
            if shuffle:
                x, y = same_shuffle(x, y)
            for batch, (x_batch, y_batch) in enumerate(zip(n_split_array(x, batch_size, keep_extra=False), n_split_array(y, batch_size, keep_extra=False))):
                zs = [x_batch]
                for layer in self.layers:
                    activation = layer.forward(zs[-1])
                    zs.append(activation)
                    
                output = zs.pop()
                                
                loss = self.loss.forward(y_batch, output, is_categorical_labels = is_categorical_labels)
                if batch % 100 == 0: print(f"{epoch=}, {batch=}, {loss=}")
                                   
                grad = self.loss.backward(y_batch, output, is_categorical_labels = is_categorical_labels)
                
                for layer, activation in zip(reversed(self.layers), reversed(zs)):
                    grad = layer.backward(activation, grad, learning_rate)