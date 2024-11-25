from ..game_events import Event
from . import Manager

class TimeManager(Manager):
    def __init__(self, fps: int) -> None:
        self.fps = fps
        self.reset()
    
    def reset(self) -> None:
        self.frame = 0
    
    def handle_event(self, event: dict[Event, object]) -> None:
        return super().handle_event(event)
    
    def tick(self):
        self.frame += 1
    
    def get_fps(self) -> int:
        return self.fps
 
    def get_frame(self) -> int:
        return self.frame

    def get_time_str(self) -> str:
        if self.fps == 0: return "Inf"

        seconds = self.frame / self.fps
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:.0f}:{seconds:0>2.0f}"