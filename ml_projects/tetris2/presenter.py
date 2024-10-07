from model import Model
from view import View

class Presenter:
    def __init__(self, tetris: Model, view: View) -> None:
        self.tetris = tetris
        self.view = view
    
    def left(self) -> None:
        self.tetris.change_x(-1)
    
    def right(self) -> None:
        self.tetris.change_x(+1)

    def rotate(self) -> None:
        self.tetris.rotate(1)
    
    def run(self) -> None:
        self.tetris.reset()