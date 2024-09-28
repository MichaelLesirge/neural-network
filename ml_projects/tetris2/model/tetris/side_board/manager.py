from abc import ABC, abstractmethod
from ..game_events import Event

class Manager(ABC):
    
    @abstractmethod
    def handle_event(self, event: dict[Event, object]) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass