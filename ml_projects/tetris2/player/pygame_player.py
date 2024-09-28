import pygame

from game_actions import Action
from .player import Player

class PygamePlayer(Player):
    DEFAULT_BINDINGS = {
        pygame.K_UP: Action.SPIN,
        pygame.K_DOWN: Action.SOFT_DROP,
        pygame.K_SPACE: Action.HARD_DROP,
        pygame.K_LEFT: Action.LEFT,
        pygame.K_RIGHT: Action.RIGHT,
        pygame.K_c: Action.HOLD,
    }

    def __init__(self, map: dict[int: Action]) -> None:
        self.map = map
 
    def get_name(self) -> str:
        return "Human Player"
    
    def get_actions(self) -> list[Action]:
        return [self.map[key] for key in pygame.key.get_pressed() if key in self.map]