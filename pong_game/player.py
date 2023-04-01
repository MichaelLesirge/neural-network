import pygame

SPEED = 3

class PaddleBase(pygame.sprite.Sprite):
    def __init__(self, screen_rect: pygame.rect.Rect, start_position: tuple[int, int], size: tuple[int, int]) -> None:
        super().__init__()
        
        self.screen_rect = screen_rect
        
        self.image = pygame.Surface(size)
        self.image.fill("white")
        
        self.rect = self.image.get_rect()
        
        self.start_x, self.start_y = start_position[0] - size[0] // 2, start_position[1] - size[1] // 2
        self.to_start_position()
    
    def to_start_position(self) -> None:
        self.x, self.y = self.start_x, self.start_y
        
    def go_up(self) -> None:
        self.y -= SPEED
        if self.rect.top <= self.screen_rect.top:
            self.y = self.screen_rect.top
    
    def go_down(self) -> None:
        self.y += SPEED
        if self.rect.bottom >= self.screen_rect.bottom:
            self.y = self.screen_rect.bottom - self.rect.height
    
    def update(self) -> None:
        self.rect.x = self.x
        self.rect.y = self.y

class HumanPaddle(PaddleBase):
    def __init__(self, screen_rect: pygame.rect.Rect, start_position: tuple[int, int], size: tuple[int, int], up_key, down_key) -> None:
        super().__init__(screen_rect, start_position, size)
        
        self.up_key = up_key
        self.down_key = down_key
        
    def update(self) -> None:
                
        keys = pygame.key.get_pressed()
        
        if keys[self.up_key]: self.go_up()
        if keys[self.down_key]: self.go_down()
        
        super().update()

class AiPaddle(PaddleBase):
    def __init__(self, screen_rect: pygame.rect.Rect, start_position: tuple[int, int], size: tuple[int, int], network) -> None:
        super().__init__(screen_rect, start_position, size)
        
        self.network = network
        
    def update(self) -> None:
        # TODO make the most complex thing I have every attempted  
        
        return super().update()


class WallPaddle(PaddleBase):
    pass