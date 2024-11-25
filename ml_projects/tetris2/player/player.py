from abc import ABC, abstractmethod
from game_actions import Action

class Player(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass


    