import pygame

from ball import Ball
from utils import RPoint


class Constants:
    SPEED = 5
    COLOR = "white"

class Paddle(pygame.sprite.Sprite):
    def __init__(self, start_position: RPoint, size: RPoint) -> None:
        super().__init__()
        
        self.start_position = start_position
        
        self.score = 0
        self.size = size
            
        self.image = pygame.Surface(self.size.point)
        self.image.fill(Constants.COLOR)
        
        self.rect = self.image.get_rect()
                
        self.rect.centery = self.start_position.y

        self.direction = 0

    def find_next_move(self, ball: Ball, screen: pygame.Surface) -> None:
        pass

    def add_score(self) -> None:
        self.score += 1
                    
    def go_up(self) -> None:
        self.rect.y -= Constants.SPEED
    
    def go_down(self) -> None:
        self.rect.y += Constants.SPEED
    
    def update(self) -> None:
        self.rect.centerx = self.start_position.x
        
        if self.direction > 0:
            self.go_up()
        elif self.direction < 0:
            self.go_down()

class HumanPaddle(Paddle):
    def __init__(self, start_position: RPoint, size: RPoint, up_key, down_key) -> None:
        super().__init__(start_position, size)
            
        self.up_key = up_key
        self.down_key = down_key
    
    def find_next_move(self, ball, screen):
        keys = pygame.key.get_pressed()
        self.direction = keys[self.up_key] - keys[self.down_key]

class BallFollowPaddle(Paddle):
    def __init__(self, start_position: RPoint, size: RPoint) -> None:
        super().__init__(start_position, size)
        self.action = None
    
    def find_next_move(self, ball: Ball, screen: pygame.Surface) -> None:
        current_y = self.rect.centery
        target_y = ball.rect.centery
        
        self.direction = current_y - target_y
    
    def update(self) -> None:
        super().update()
        if self.action: self.action()

class WallPaddle(Paddle):
    def __init__(self, start_position: RPoint, size: RPoint) -> None:
        size._y = 1
        super().__init__(start_position, size)  