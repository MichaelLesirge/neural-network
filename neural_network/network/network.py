import pickle

import numpy as np

from neural_network.losses.losses import Loss
from neural_network.base import BaseLayer


# at some point add compile step where optimizations could be made and Dense Layers could find how many inputs they have
#  _init_params should also return self and any other layers to add (for example Dense could return itself and an activation)
# also save _init_params for model save / load

def n_split_array(arr, n_size, *, keep_extra=True):
    """split arr into chunks of size n with extra added on end if keep_extra is true"""
    if n_size is None: return arr
        
    if len(arr) < n_size:
        return [arr] if keep_extra else []
    
    div, extra = divmod(len(arr), n_size)
    
    a, b = np.split(arr, [len(arr) - extra])
    
    return np.array_split(a, div) + ([b] if (len(b) and keep_extra) else [])


def same_shuffle(*arrays):
    """shuffle 2 arrays """
    order = np.arange(np.size(arrays[0], 0))
    np.random.shuffle(order)
    return tuple(array[order] for array in arrays)

class Network:
    def __init__(self, layers: list[BaseLayer], loss: Loss, preprocess: list = []) -> None:
        self.layers = layers
        self.loss = loss
        self.reprocesses = preprocess
    
    def compute(self, inputs: np.ndarray) -> np.ndarray:
        
        for proc in self.reprocesses:
            inputs = proc(inputs)
        
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs
    
    
    def train(self, x: np.ndarray, y: np.ndarray, learning_rate: float = 0.001, batch_size: int = 32, epochs: int = 1, shuffle: bool = True, logging = True):

        for proc in self.reprocesses:
            x = proc(x)
            
        max_str_len = 0
        
        loss = None
        
        last_percent_complete = -1
         
        for epoch in range(epochs):
            if shuffle:
                x, y = same_shuffle(x, y)
            x_split, y_split = n_split_array(x, batch_size), n_split_array(y, batch_size)
            for batch, (x_batch, y_batch) in enumerate(zip(x_split, y_split)):                      
                zs = [x_batch]
                for layer in self.layers:
                    activation = layer.forward(zs[-1])
                    zs.append(activation)
                    
                # todo add more logging options and make it so it ends at 100 and batch at 50 by +1
                    
                output = zs.pop()
                                
                loss = self.loss.forward(y_batch, output)
                
                percent_complete = int((batch + len(x_split) * epoch) / (len(x_split) * epochs) * 100)
                if logging and (percent_complete > last_percent_complete or batch == 0):
                    last_percent_complete = percent_complete
                    message = f"{percent_complete}% complete. {epoch=}, {batch=}, {loss=}"
                    max_str_len = max(max_str_len, len(message))
                    print(message.ljust(max_str_len), end=("\n" if batch == 0 else "\r"))
                                   
                grad = self.loss.backward(y_batch, output)
                
                for layer, activation in zip(reversed(self.layers), reversed(zs)):
                    grad = layer.backward(activation, grad, learning_rate)
            
        if logging: print(f"100% complete. finished, {loss=}".ljust(max_str_len))
 
    def dump(self, file_path: str) -> None:
        with open(file_path.lstrip(".pkl") + ".pkl", "wb") as file:
            file.write(self.dumps())
    
    def dumps(self) -> bytes:
        return pickle.dumps(
            tuple(layer.save_params() for layer in self.layers)
        )
    
    def load(self, file_pah: str) -> None:
        with open(file_pah + ".pkl", "rb") as file:
            self.loads(file.read())
    
    def loads(self, params: bytes) -> None:
        for layer, saved_layer_data in zip(self.layers, pickle.loads(params)):
            layer.load_params(saved_layer_data)