import pygame

from ball import Ball
from utils import RelativeRectPoint


class Constants:
    SPEED = 5
    COLOR = "white"

class Paddle(pygame.sprite.Sprite):
    def __init__(self, start_position: RelativeRectPoint, size: RelativeRectPoint) -> None:
        super().__init__()
        
        self.start_position = start_position
        
        self.score = 0
        self.size = size
            
        self.image = pygame.Surface(self.size.point)
        self.image.fill(Constants.COLOR)
        
        self.rect = self.image.get_rect()
                
        self.rect.centery = self.start_position.y
        
    def add_score(self) -> None:
        self.score += 1
                    
    def go_up(self) -> None:
        self.rect.y -= Constants.SPEED
    
    def go_down(self) -> None:
        self.rect.y += Constants.SPEED
    
    def update(self) -> None:
        self.rect.centerx = self.start_position.x

class HumanPaddle(Paddle):
    def __init__(self, start_position: RelativeRectPoint, size: RelativeRectPoint, up_key, down_key) -> None:
        super().__init__(start_position, size)
            
        self.up_key = up_key
        self.down_key = down_key
        
    def update(self) -> None:
        super().update()
                
        keys = pygame.key.get_pressed()
        
        if keys[self.up_key]: self.go_up()
        if keys[self.down_key]: self.go_down()
        
        

class AiPaddle(Paddle):
    def __init__(self, start_position: RelativeRectPoint, size: RelativeRectPoint) -> None:
        super().__init__(start_position, size)
        self.action = None
    
    def find_next_move(self, ball: Ball, screen: pygame.Surface) -> None:
        y = self.rect.centery
        ball_y = ball.rect.centery
        
        difference = y - ball_y
        
        if difference > 5:
            self.action = self.go_up
        elif difference < 5:
            self.action = self.go_down
        else:
            self.action = None
    
    def update(self) -> None:
        super().update()
        if self.action: self.action()

class WallPaddle(Paddle):
    def __init__(self, start_position: RelativeRectPoint, size: RelativeRectPoint) -> None:
        size._y = 1
        super().__init__(start_position, size)  