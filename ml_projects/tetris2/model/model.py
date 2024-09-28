from game_actions import Action
from game_state import State

class Model:

    def reset(self) -> None:
        pass
    
    def update(actions: list[Action]) -> State:
        return State(None, None, 0, None, None, False, {})