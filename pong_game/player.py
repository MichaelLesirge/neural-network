import pygame
from utils import rect_centered_point 

SPEED = 5

class PaddleBase(pygame.sprite.Sprite):
    def __init__(self, start_position: tuple[int, int], size: tuple[int, int]) -> None:
        super().__init__()
        
        self.score = 0
        
        self.image = pygame.Surface(size)
        self.image.fill("white")
        
        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = rect_centered_point(self.rect, start_position)
        self.start_position = start_position
        
    def add_score(self) -> None:
        self.score += 1
                    
    def go_up(self) -> None:
        self.rect.y -= SPEED
    
    def go_down(self) -> None:
        self.rect.y += SPEED
    
    def update(self) -> None:
        pass

class HumanPaddle(PaddleBase):
    def __init__(self, start_position: tuple[int, int], size: tuple[int, int], up_key, down_key) -> None:
        super().__init__(start_position, size)
            
        self.up_key = up_key
        self.down_key = down_key
        
    def update(self) -> None:
                
        keys = pygame.key.get_pressed()
        
        if keys[self.up_key]: self.go_up()
        if keys[self.down_key]: self.go_down()
        
        super().update()
        

class AiPaddle(PaddleBase):
    def __init__(self, start_position: tuple[int, int], size: tuple[int, int], network) -> None:
        super().__init__(start_position, size)
        
        self.network = network
        
    def update(self) -> None:
        # TODO make the most complex thing I have every attempted  
        
        return super().update()


class WallPaddle(PaddleBase):
    pass