from . import Manager

class ScoreManger(Manager):
    
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.score = 0