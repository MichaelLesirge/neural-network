from abc import ABC, abstractmethod
from tetris import Action

class Player(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_actions(self) -> list[Action]:
        pass

    