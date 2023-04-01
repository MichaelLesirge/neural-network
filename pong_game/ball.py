import pygame

SIZE = (10, 10)

def classic_round(x):
    i, f = divmod(x, 1)
    return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen_rect: pygame.rect.Rect, start_position: tuple[int, int], slope: float, velocity: float) -> None:
        super().__init__()
        
        self.screen_rect = screen_rect
        
        self.image = pygame.Surface(SIZE)
        self.image.fill("white")

        self.rect = self.image.get_rect()

        self.x, self.y = start_position[0] - SIZE[0] // 2, start_position[1] - SIZE[1] // 2

        slope_rise, slope_run = slope.as_integer_ratio()
        self.x_velocity, self.y_velocity = slope_run / slope_run * velocity, slope_rise / slope_run * velocity

    def bounce_y(self) -> None:
        self.y_velocity *= -1

    def bounce_x(self) -> None:
        self.x_velocity *= -1

    def add_velocity(self, amount: float) -> None:
        self.x_velocity += amount
        self.y_velocity += amount

    def update(self) -> None:
        self.x += self.x_velocity
        self.y += self.y_velocity
        
        self.rect.x = classic_round(self.x)
        self.rect.y = classic_round(self.y)
        
        if self.rect.top < self.screen_rect.top or self.rect.bottom > self.screen_rect.bottom:
            self.bounce_y()
        