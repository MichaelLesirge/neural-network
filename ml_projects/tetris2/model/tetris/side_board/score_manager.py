from ..game_events import Event
from . import Manager

class ScoreManger(Manager):
    
    def __init__(self, for_line_clear: list[int], for_events: dict[Event, int]) -> None:
        self.for_line_clear = for_line_clear
        self.for_action = for_events
        self.reset()
    
    def handle_event(self, event: dict[Event, object]) -> None:
        return super().handle_event(event)

    def reset(self) -> None:
        self.score = 0