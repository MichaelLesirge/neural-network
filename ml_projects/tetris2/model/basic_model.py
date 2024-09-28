from game_actions import Action
from game_state import State
from .model import Model

class BasicModel(Model):
    def update(actions: list[Action]) -> State:
        pass