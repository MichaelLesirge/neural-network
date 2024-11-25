from game_actions import Action
from game_state import State
from .player import Player


class AlgorithmPlayer(Player):
    def __init__(self) -> None:
        pass
 
    def get_name(self) -> str:
        return "Algorithm Player"
    
    def get_actions(self, state: State) -> list[Action]:
        return [Action.HARD_DROP]