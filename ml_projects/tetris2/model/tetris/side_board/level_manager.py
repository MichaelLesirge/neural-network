from ..game_events import Event
from . import Manager

class LevelManager(Manager):
    def __init__(self, lines_for_next_level: int) -> None:
        self.lines_for_next_level = lines_for_next_level
        self.reset()

    def reset(self) -> None:
        self.lines_cleared = 0
        self.level = 1
    
    def handle_event(self, event: dict[Event, object]) -> None:
        for event, data in event.items():
            if event == Event.LINE_CLEAR:
                self.lines_cleared += data
                self.level = self.lines_cleared // self.lines_for_next_level + 1

    def get_level(self) -> int:
        return self.level

    def get_drop_interval_seconds(self) -> float:
        if self.level < 11: frame_interval = 60 - self.level * 5
        elif self.level < 12: frame_interval = 9
        elif self.level < 13: frame_interval = 8
        elif self.level < 15: frame_interval = 7
        elif self.level < 17: frame_interval = 6
        elif self.level < 20: frame_interval = 5
        elif self.level < 24: frame_interval = 4
        elif self.level < 29: frame_interval = 3
        elif self.level < 30: frame_interval = 3
        else: frame_interval = 1

        return frame_interval / 60
    
    def get_time_till_freeze_seconds(self) -> float:
        return self.get_drop_interval_seconds()
