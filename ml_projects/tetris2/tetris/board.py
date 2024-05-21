import numpy as np

class Board:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        
        self.reset()
    
    def reset(self):
        self.grid = np.zeros((self.height, self.width), dtype=np.uint8)