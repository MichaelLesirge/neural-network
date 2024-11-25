import typing

import pygame

from._common import Coordinate, Color

Runnable = typing.Callable[[], None]

def _run(actions: list[Runnable]) -> None:
    for action in actions:
        action()

class TextButton:    
    def __init__(self, text: str, outline_color: Color = "white", background_color: Color = "black", text_color: Color = "white") -> None:
        self.position: pygame.Vector2 = None
                        
        self.text = text

        self.outline_color = outline_color
        self.background_color = background_color
        self.text_color = text_color
        
        self.was_mouse_down = self.enabled = self.is_pressed = self.is_hovered = False

        self.on_hovered_actions: list[Runnable] = []
        self.on_pressed_actions: list[Runnable] = []
            
    def add_hovered_action(self, func: Runnable) -> None:
        self.on_hovered_actions.append(func)

    def add_pressed_action(self, func: Runnable) -> None:
        self.on_pressed_actions.append(func)

    def is_over(self, position: Coordinate) -> bool:
        if self.position is None:
            return False
        return pygame.rect.Rect(self.position, self.size).collidepoint(position)

    def update(self, mouse_position: Coordinate, mouse_down: bool = False) -> None:
        
        was_hovered = self.is_hovered
        self.is_hovered = self.is_over(mouse_position)

        if not was_hovered and self.is_hovered:
            _run(self.on_hovered_actions)

        self.is_pressed = self.is_hovered and mouse_down
         
        if self.is_pressed and not self.was_mouse_down:
            _run(self.on_pressed_actions)
        
        self.was_mouse_down = mouse_down

    def get_image(self) -> pygame.Surface:
        
        image = pygame.Surface(self.size)

        image.fill(self.background_color)
        pygame.draw.rect(image, self.outline_color, image.get_rect(), 3)

        font = pygame.font.Font(None, 30)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=image.get_rect().center)
        image.blit(text, text_rect)

        if self.is_pressed:
            brighten = 59
            image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_SUB) 
        elif self.is_hovered:
            brighten = 128
            image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 

        return image
    
    def put_at_position(self, surface: pygame.Surface, position: Coordinate, size: Coordinate) -> None:
        self.position = pygame.Vector2(position)
        self.size = size

        surface.blit(self.get_image(), self.position)