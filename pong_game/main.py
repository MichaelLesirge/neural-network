import pygame
from ball import Ball
from player import HumanPaddle, AiPaddle, WallPaddle

def make_screen_size(size_px: int, aspect_ration: float, horizontal: bool = True):
    return int(size_px * ((aspect_ration * (horizontal)) or 1)), int(size_px * ((aspect_ration * (not horizontal)) or 1))

def to_size_relitive_value(size: int, value: float, reverse = False) -> int:
    relitive_point = int(size * value)
    if reverse: relitive_point = size - relitive_point
    return relitive_point

def to_rect_relitive_points(screen: pygame.rect.Rect, point: tuple[float, float], reverse_x = False, reverse_y = False) -> tuple[int, int]:
    return to_size_relitive_value(screen.width, point[0], reverse_x), to_size_relitive_value(screen.height, point[1], reverse_y)

WINDOW_NAME = "Pong Game"
FRAMERATE = 60

BALL_START_LOCATION = (0.7, 0.1)
BALL_START_SLOPE = -1 / 2
BALL_VELOCITY = -2
BALL_BOUNCE_VELOCITY_INCREACE = 0.1

PADDLE_START_LOCATION = (0.06, 0.5)
NORMAL_PADDLE_SIZE = (0.01, 0.2)

def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)

    screen = pygame.display.set_mode(make_screen_size(
        size_px=400, aspect_ration=16/10, horizontal=True))
    screen_rect = screen.get_rect()
    
    
    clock = pygame.time.Clock()

    ball = Ball(
        screen_rect,
        start_position = to_rect_relitive_points(screen_rect, BALL_START_LOCATION),
        slope = BALL_START_SLOPE, velocity = BALL_VELOCITY)

    player1 = HumanPaddle(
        screen_rect,
        to_rect_relitive_points(screen_rect, PADDLE_START_LOCATION, reverse_x = False),
        to_rect_relitive_points(screen_rect, NORMAL_PADDLE_SIZE),
        pygame.K_q, pygame.K_a
    )
    
    player2 = HumanPaddle(
        screen_rect,
        to_rect_relitive_points(screen_rect, PADDLE_START_LOCATION, reverse_x = True),
        to_rect_relitive_points(screen_rect, NORMAL_PADDLE_SIZE),
        pygame.K_p, pygame.K_l
    )

    all_sprites = pygame.sprite.Group(ball, player1, player2) # type: ignore

    running = True
    while running:
        screen.fill("black")
        pygame.draw.line(screen, "white", to_rect_relitive_points(screen_rect, (0.5, 0)), to_rect_relitive_points(screen_rect, (0.5, 1)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                 
        all_sprites.update()
        
        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
            ball.bounce_x()
            ball.add_velocity(BALL_BOUNCE_VELOCITY_INCREACE)
        
        all_sprites.draw(screen)
        pygame.display.update()

        clock.tick(FRAMERATE)
    
    pygame.quit()


if __name__ == "__main__":
    main()
