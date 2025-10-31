import pygame

from utils import ScreenRelativeVector2 as RelVec2

class Ball(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, size: int) -> None:
        super().__init__()

        self.screen = surface

        self.image = pygame.Surface((size, size))
        self.image.fill("white")
        
        self.rect = self.image.get_rect() 

        self.position = RelVec2()
        self.velocity = RelVec2()
    
    def set_position(self, position: RelVec2) -> None:
        self.position = RelVec2(position)

    def set_velocity(self, velocity: RelVec2) -> None:
        self.velocity = RelVec2(velocity)
        
    def bounce_x(self) -> None:
        self.velocity.x = -self.velocity.x

    def bounce_y(self) -> None:
        self.velocity.y = -self.velocity.y
    
    def update(self) -> None:
        self.position += self.velocity

        self.rect.center = self.position.to_pixels(self.screen)
        