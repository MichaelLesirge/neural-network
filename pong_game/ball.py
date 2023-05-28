import pygame
from utils import RelitiveRectPoint

class Ball(pygame.sprite.Sprite):
    def __init__(self, size: int, start_position: RelitiveRectPoint, start_slope: tuple[int, int], start_velocity: int, max_velocity: int) -> None:
        super().__init__()   
        self.image = pygame.Surface((size, size))
        self.image.fill("white")
        
        self.rect = self.image.get_rect() 

        self.start_velocity = start_velocity
        self.max_velocity = max_velocity
        
        self.start_position = start_position
        self.start_slope = start_slope
        self.to_starting_position()
        
    
    def set_new_motion(self, position: RelitiveRectPoint, slope: tuple[int, int]) -> None:
        self.velocity = self.start_velocity
        
        self.rect.center = position.point
        self.y_change, self.x_change = slope
    
    def to_starting_position(self, to_reverse_side = False):
        self.set_new_motion(self.start_position.flip(flip_x=to_reverse_side), (self.start_slope[0], self.start_slope[1] * (-1 if to_reverse_side else 1)))
        
    def bounce_y(self) -> None:
        self.y_change *= -1

    def bounce_x(self) -> None:
        self.x_change *= -1
    
    @property
    def x_velocity(self) -> int:
        return int(self.x_change * self.velocity)
    
    @property
    def y_velocity(self) -> int:
        return int(self.y_change * self.velocity)

    def add_velocity(self, amount: float) -> None:
        self.velocity = min(self.velocity + amount, self.max_velocity)

    def update(self) -> None:
        self.rect.centerx += self.x_velocity
        self.rect.centery += self.y_velocity
        