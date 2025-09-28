import pygame
import time

from game_actions import Action
from .player import Player

class Trigger:
    def __init__(self, action: Action, repeat_delay_millisecond: int = None, repeat_interval_millisecond: int = None) -> None:
        self.action = action
        self.delay = repeat_delay_millisecond
        self.interval = repeat_interval_millisecond

        self.initial = False
        self.clock = None
        self.actions = []
    
    def pressed(self):
        self.clock = (time.time() + self.delay) if self.delay is not None else None
        self.actions.append(self.action)
        
    def released(self):
        self.clock = None
    
    def check_for_actions(self) -> bool:
        if self.clock is not None and self.clock <= time.time():
            self.clock =  (time.time() + self.interval) if self.interval is not None else None
            self.actions.append(self.action)
                
        return len(self.actions) > 0

    def get_action(self) -> Action:
        return self.actions.pop(0) if len(self.actions) > 0 else None

class PygamePlayer(Player):
    DEFAULT_BINDINGS = {
        pygame.K_UP: Trigger(Action.SPIN),
        pygame.K_DOWN: Trigger(Action.SOFT_DROP, 0, 0),
        pygame.K_SPACE: Trigger(Action.HARD_DROP),
        pygame.K_LEFT: Trigger(Action.LEFT, 0.170, 0.050),
        pygame.K_RIGHT: Trigger(Action.RIGHT, 0.170, 0.050),
        pygame.K_c: Trigger(Action.HOLD)
    }

    def __init__(self, control_map: dict[int, Trigger]) -> None:
        pygame.init()

        self.control_map = control_map
 
    def get_name(self) -> str:
        return "Human Player"
    
    def get_actions(self, events: list[pygame.event.Event]) -> list[Action]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.control_map:
                    self.control_map[event.key].pressed()
            if event.type == pygame.KEYUP:
                if event.key in self.control_map:
                    self.control_map[event.key].released()
        
        return [trigger.get_action() for trigger in self.control_map.values() if trigger.check_for_actions()]
            