import pygame

from button import Button
from utils import RPoint

class Chooser:
    def __init__(self, screen: pygame.Surface, options: list[str], position: RPoint, button_size: RPoint, gap: float) -> None:
        self.options = {
            option: Button(option, RPoint(screen, (position._x, position._y + i * (button_size._y + gap))), button_size, self.select)
            for i, option in enumerate(options)
        }

        self.group = pygame.sprite.Group(self.options.values())

        self.select(list(self.options.values())[0])
    
    def select(self, button: Button) -> None:
        for other_button in self.options.values():
            other_button.set_state(other_button is button)

    def get(self) -> str:
        for option, button in self.options.items():
            if button.get():
                return option
        raise ValueError("No option selected")
    
    def update(self, mouse_pos: tuple[int, int], mouse_down: bool = False) -> None:
        self.group.update(mouse_pos, mouse_down)

    def draw(self, screen: pygame.Surface) -> None:
        self.group.draw(screen)