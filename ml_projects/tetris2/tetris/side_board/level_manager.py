from . import Manager

class LevelManager(Manager):
    def __init__(self, lines_for_next_level: int) -> None:
        self.lines_for_next_level = lines_for_next_level
        self.reset()

    def reset(self) -> None:
        self.level = 0

    def get_level(self) -> int:
        return self.level