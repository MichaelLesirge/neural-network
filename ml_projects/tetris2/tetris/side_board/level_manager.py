from ..game_events import Event
from . import Manager

class LevelManager(Manager):
    def __init__(self, lines_for_next_level: int) -> None:
        self.lines_for_next_level = lines_for_next_level
        self.reset()

    def reset(self) -> None:
        self.level = 0
    
    def handle_event(self, event: dict[Event, object]) -> None:
        return super().handle_event(event)

    def get_level(self) -> int:
        return self.level