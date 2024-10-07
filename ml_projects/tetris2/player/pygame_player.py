import pygame

from game_actions import Action
from presenter import Presenter

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

    def __init__(self, control_map: dict[int: Action]) -> None:
        pygame.init()

        self.control_map = control_map
 
    def get_name(self) -> str:
        return "Human Player"
    
    def get_actions(self, presenter: Presenter) -> list[Action]:
        pressed = pygame.key.get_pressed()
        return [action for (key, action) in self.control_map.items() if pressed[key]]