import pygame
import ball
from utils import RelativeRectPoint

class Contants:
    SPEED = 5
    COLOR = "white"

class PaddleBase(pygame.sprite.Sprite):
    def __init__(self, start_position: RelativeRectPoint, size: RelativeRectPoint) -> None:
        super().__init__()
        
        self.score = 0
        self.size = size
            
        self.image = pygame.Surface(self.size.point)
        self.image.fill(Contants.COLOR)
        
        self.rect = self.image.get_rect()
                
        self.rect.centerx, self.rect.centery = start_position.point
        self.start_position = start_position
        
    def add_score(self) -> None:
        self.score += 1
                    
    def go_up(self) -> None:
        self.rect.y -= Contants.SPEED
    
    def go_down(self) -> None:
        self.rect.y += Contants.SPEED
    
    def update(self) -> None:
        self.rect.x = self.start_position.x

class HumanPaddle(PaddleBase):
    def __init__(self, start_position: RelativeRectPoint, size: RelativeRectPoint, up_key, down_key) -> None:
        super().__init__(start_position, size)
            
        self.up_key = up_key
        self.down_key = down_key
        
    def update(self) -> None:
                
        keys = pygame.key.get_pressed()
        
        if keys[self.up_key]: self.go_up()
        if keys[self.down_key]: self.go_down()
        
        super().update()
        

class AiPaddle(PaddleBase):
    def __init__(self, start_position: RelativeRectPoint, size: RelativeRectPoint, network) -> None:
        super().__init__(start_position, size)
        
        self.network = network
        self.action = None
    
    def update_network(self, ball: ball.Ball, screen, other_player) -> None:
        # data = [*self.rect.topleft, *self.rect.bottomright, *other_player.topleft, *other_player.topleft, *other_player.bottomright,
        #         *ball.rect.center, ball.x_velocity, ball.y_velocity,
        #         screen.]
        pass
        
        
    def update(self) -> None:
        # TODO make the most complex thing I have every attempted  
        
        return super().update()


class WallPaddle(PaddleBase):
    pass