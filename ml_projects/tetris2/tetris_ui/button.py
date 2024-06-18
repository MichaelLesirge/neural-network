import typing

import pygame

Runnable = typing.Callable[[], None]

xyPair = tuple[int, int] | pygame.Vector2

def _run(actions: list[Runnable]) -> None:
    for action in actions:
        action()

class ToggleButton:    
    def __init__(self, enable_image: pygame.Surface, disable_image: pygame.Surface) -> None:

        self.position: pygame.Vector2 = None
        self.radius: int = None
                        
        self.enable_image = enable_image
        self.disable_image = disable_image
        
        self.enabled = self.is_clicked = self.is_hovered = False

        self.on_hovered_actions: list[Runnable] = []
        self.on_pressed_actions: list[Runnable] = []

        self.on_toggled_action: list[Runnable] = []
        self.on_enabled_actions: list[Runnable] = []
        self.on_disabled_actions: list[Runnable] = []
            
    def add_hovered_action(self, func: Runnable) -> None:
        self.on_hovered_actions.append(func)

    def add_pressed_action(self, func: Runnable) -> None:
        self.on_pressed_actions.append(func)

    def add_toggled_action(self, func: Runnable) -> None:
        self.on_toggled_action.append(func)

    def add_enabled_action(self, func: Runnable) -> None:
        self.on_enabled_actions.append(func)

    def add_disabled_action(self, func: Runnable) -> None:
        self.on_disabled_actions.append(func)

    def is_over(self, position: xyPair) -> bool:
        if self.position is None:
            return False
        return pygame.Vector2(position).distance_to(self.position) <= self.radius

    def update(self, mouse_position: xyPair, mouse_down: bool = False) -> None:
        
        was_hovered = self.is_hovered
        self.is_hovered = self.is_over(mouse_position)

        if not was_hovered and self.is_hovered:
            _run(self.on_hovered_actions)

        self.is_clicked = self.is_hovered and mouse_down
         
        if self.is_clicked:
            self.toggle_state()
            _run(self.on_pressed_actions)
        
    def get_image(self) -> pygame.Surface:
        image = self.enable_image if self.enabled else self.disable_image
        image = pygame.transform.scale(image, self.size)
        image = pygame.transform.scale_by(image, 1 + (-0.2 if self.is_clicked else 0) + (0.1 if self.is_hovered else 0))
        return image
    
    def put_at_position(self, surface: pygame.Surface, position: xyPair, circumference: int):
        self.position = pygame.Vector2(position)
        self.radius = circumference / 2
        self.size = pygame.Vector2(circumference, circumference)

        surface.blit(self.get_image(), self.position - (pygame.Vector2(self.get_image().get_size()) / 2))
        
    def enable(self) -> None:
        self.enabled = True

        _run(self.on_enabled_actions)

    def disable(self) -> None:
        self.enabled = False

        _run(self.on_disabled_actions)

    def toggle_state(self) -> None:
        self.enabled = not self.enabled

        _run(self.on_toggled_action + (self.on_enabled_actions if self.enabled else self.on_disabled_actions))
        
    def is_enabled(self) -> bool:
        return self.enabled