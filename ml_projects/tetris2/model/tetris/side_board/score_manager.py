from ..game_events import Event
from . import Manager

class ScoreManger(Manager):
    
    def __init__(self, for_line_clear: list[int], for_events: dict[Event, int]) -> None:
        self.for_line_clear = for_line_clear
        self.for_action = for_events
        self.reset()
    
    def handle_event(self, event: dict[Event, object]) -> None:
        for event, data in event.items():
            if event in self.for_action:
                self.score += self.for_action[event] * data
            if event == Event.LINE_CLEAR:
                self.score += self.for_line_clear[min(data, len(self.for_line_clear) - 1)]
                self.lines_cleared += data

    def get_score(self) -> int:
        return self.score
    
    def get_lines_cleared(self) -> int:
        return self.lines_cleared

    def reset(self) -> None:
        self.score = 0
        self.lines_cleared = 0