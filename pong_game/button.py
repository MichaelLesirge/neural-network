import pygame

from utils import ScreenRelativeVector2

class Button(pygame.sprite.Sprite):
    TEXT_COLOR = "white"
    OUTLINE_COLOR = "white"
    BACKGROUND_COLOR = "black"
    ENABLED_COLOR = (50, 0, 100)

    def __init__(self, screen: pygame.Surface, name: str, position: ScreenRelativeVector2, size: ScreenRelativeVector2) -> None:
        super().__init__()

        self.screen = screen
        self.name = name
        self.position = position
        self.size = size

        self.state = self.is_pressed = self.is_hovered = False
        
        self.image = self.generate_image()
        self.rect = self.image.get_rect(center=self.position.to_pixels(self.screen))

        self.on_toggle = []

    def generate_image(self) -> pygame.Surface:
        image = pygame.Surface(self.size.to_pixels(self.screen))

        if self.get():
            image.fill(self.ENABLED_COLOR)

        font = pygame.font.Font(None, image.get_height())
        text_surface = font.render(self.name, True, self.TEXT_COLOR)

        pygame.draw.rect(image, self.OUTLINE_COLOR, image.get_rect(), 3)

        image.blit(text_surface, text_surface.get_rect(center=image.get_rect().center))
        image = pygame.transform.scale_by(image, 1 + (-0.2 if self.is_pressed else 0) + (0.1 if self.is_hovered else 0))

        return image

    def update(self, mouse_pos: tuple[int, int], mouse_down: bool = False) -> None:
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        was_clicked = self.is_pressed
        self.is_pressed = self.is_hovered and mouse_down

        # Detect button release
        if was_clicked and not self.is_pressed and self.is_hovered:
            self.toggle()
        
        self.image = self.generate_image()
        self.rect = self.image.get_rect(center=self.position.to_pixels(self.screen))

    def add_toggle_listener(self, callback) -> None:
        self.on_toggle.append(callback)

    def toggle(self) -> None:
        self.state = not self.state
        for callback in self.on_toggle:
            callback(self)

    def set_state(self, state: bool) -> None:
        self.state = state

    def get_name(self):
        return self.name

    def get(self) -> bool:
        return self.state