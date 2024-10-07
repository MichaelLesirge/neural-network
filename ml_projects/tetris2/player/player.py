from game_actions import Action
from presenter import Presenter

class Player:

    def get_name(self) -> str:
        return "Player"

    def get_actions(self, presenter: Presenter) -> list[Action]:
        return []

    