import pygame
from utils import rect_centered_point 

class Ball(pygame.sprite.Sprite):
    def __init__(self, size: int, start_position: tuple[int, int], start_slope: tuple[int, int], start_velocity: int, max_velocity: int) -> None:
        super().__init__()        
        self.image = pygame.Surface((size, size))
        self.image.fill("white")

        self.rect = self.image.get_rect()
        
        self.start_velocity = 10
        self.max_velocity = max_velocity
        
        self.set_new_motion(start_position, start_slope)
        
    def set_new_motion(self, position: tuple[int, int], slope: tuple[int, int]) -> None:
        self.velocity = self.start_velocity
        
        self.rect.center = position
        self.y_velocity, self.x_velocity = slope
        
    def bounce_y(self) -> None:
        self.y_velocity *= -1

    def bounce_x(self) -> None:
        self.x_velocity *= -1

    def add_velocity(self, amount: float) -> None:
        self.velocity = min(self.velocity + amount, self.max_velocity)

    def update(self) -> None:
        self.rect.centerx += int(self.x_velocity * self.velocity)
        self.rect.centery += int(self.y_velocity * self.velocity)
        