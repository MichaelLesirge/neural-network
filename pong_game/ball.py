import pygame
from utils import rect_centered_point 

def classic_round(x):
    i, f = divmod(x, 1)
    return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))

class Ball(pygame.sprite.Sprite):
    def __init__(self, size: int, start_position: tuple[int, int], start_slope: float, start_velocity: float, max_velocity: float) -> None:
        super().__init__()        
        self.image = pygame.Surface((size, size))
        self.image.fill("white")

        self.rect = self.image.get_rect()
        
        self.max_velocity = max_velocity

        self.set_motion(start_position, start_slope, start_velocity)
        
    def set_motion(self, position: tuple[int, int], slope: float, velocity: float) -> None:
        self.x, self.y = position
        
        self.velocity = velocity

        slope_rise, slope_run = slope.as_integer_ratio()
        self.y_velocity, self.x_velocity = slope_run / slope_run, slope_rise / slope_run
 
    def bounce_y(self) -> None:
        self.y_velocity *= -1

    def bounce_x(self) -> None:
        self.x_velocity *= -1

    def add_velocity(self, amount: float) -> None:
        self.velocity = min(self.velocity + amount, self.max_velocity)

    def update(self) -> None:        
        self.x += self.x_velocity * self.velocity
        self.y += self.y_velocity * self.velocity
        
        self.rect.center = classic_round(self.x), classic_round(self.y)
        