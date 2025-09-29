import pygame

from utils import RPoint

class Button(pygame.sprite.Sprite):
    def __init__(self, text: str, position: RPoint, size: RPoint, on_toggle = None) -> None:
        super().__init__()
        self.text = text
        self.position = position
        self.size = size
        self.on_toggle = on_toggle

        self.font = pygame.font.Font(None, self.size.y)
        
        self.image = pygame.Surface(self.size.point)
        self.rect = self.image.get_rect()

        self.state = self.is_clicked = self.is_hovered = False

    def update(self, mouse_pos: tuple[int, int], mouse_down: bool = False) -> None:
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        was_clicked = self.is_clicked
        self.is_clicked = self.is_hovered and mouse_down

        if self.is_clicked and not was_clicked:
            self.toggle()

        self.image = pygame.Surface(self.size.point)

        if self.get():
            self.image.fill((50, 0, 100))

        text_color = "white"
        text_surface = self.font.render(self.text, True, text_color)

        outline_color = "white"
        pygame.draw.rect(self.image, outline_color, self.image.get_rect(), 3)

        self.image.blit(text_surface, text_surface.get_rect(center=self.image.get_rect().center))
        self.image = pygame.transform.scale_by(self.image, 1 + (-0.1 if self.is_clicked else 0) + (0.05 if self.is_hovered else 0))
        self.rect = self.image.get_rect(center=self.position.point)

    def toggle(self) -> None:
        self.state = not self.state
        if self.on_toggle:
            self.on_toggle(self)

    def set_state(self, state: bool) -> None:
        self.state = state

    def get(self) -> bool:
        return self.state