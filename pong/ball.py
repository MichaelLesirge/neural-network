import pygame

from utils import ScreenRelativeVector2 as RelVec2

class Ball(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, size: int) -> None:
        super().__init__()

        self.screen = surface

        self.image = pygame.Surface((size, size))
        self.image.fill("white")
        
        self.rect = self.image.get_rect() 

        self.collision_check_function = lambda: False

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

    def set_collision_handler(self, func) -> None:
        self.collision_check_function = func
    
    def update(self) -> None:

        subdivisions = int(self.velocity.to_pixels(self.screen).magnitude() // 2) + 1
        
        for _ in range(subdivisions):
            self.position += self.velocity / subdivisions
            self.rect.center = self.position.to_pixels(self.screen)
            if self.collision_check_function():
                break
        