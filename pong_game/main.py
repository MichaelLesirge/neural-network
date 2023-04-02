import pygame
from ball import Ball
from player import HumanPaddle, AiPaddle, WallPaddle
from utils import to_rect_relitive_points


def make_screen_size(size_px: int, aspect_ration: float, horizontal: bool = True):
    return int(size_px * ((aspect_ration * (horizontal)) or 1)), int(size_px * ((aspect_ration * (not horizontal)) or 1))


WINDOW_NAME = "Pong Game"
FRAMERATE = 60

BALL_SIZE = 10
BALL_MAX_VELOCITY = 6

BALL_START_LOCATION = 0.07, 0.1
BALL_START_SLOPE = 2 / 1
BALL_START_VELOCITY = 2
BALL_BOUNCE_VELOCITY_INCREACE = 0.1

PADDLE_START_LOCATION = 0.06, 0.5
NORMAL_PADDLE_SIZE = 0.01, 0.2


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)

    screen = pygame.display.set_mode(
        make_screen_size(size_px=400, aspect_ration=16/10, horizontal=True)
    )
    
    screen_rect = screen.get_rect()

    clock = pygame.time.Clock()

    ball = Ball(
        BALL_SIZE, to_rect_relitive_points(screen_rect, BALL_START_LOCATION),
        BALL_START_SLOPE, BALL_START_VELOCITY, BALL_MAX_VELOCITY
    )

    player1 = HumanPaddle(
        to_rect_relitive_points(screen_rect, PADDLE_START_LOCATION, reverse_x=False),
        to_rect_relitive_points(screen_rect, NORMAL_PADDLE_SIZE),
        pygame.K_q, pygame.K_a
    )

    player2 = HumanPaddle(
        to_rect_relitive_points(screen_rect, PADDLE_START_LOCATION, reverse_x=True),
        to_rect_relitive_points(screen_rect, NORMAL_PADDLE_SIZE),
        pygame.K_p, pygame.K_l
    )

    all_sprites = pygame.sprite.Group(ball, player1, player2)  # type: ignore

    running = True
    while running:
        screen.fill("black")
        pygame.draw.line(screen, "white",
                        to_rect_relitive_points(screen_rect, (0.5, 0)),
                        to_rect_relitive_points(screen_rect, (0.5, 1)))

        if pygame.event.get(pygame.QUIT):
            running = False

        all_sprites.update()

        player1.rect.clamp_ip(screen_rect)
        player2.rect.clamp_ip(screen_rect)

        if ball.rect.collideobjects((player1.rect, player2.rect)):
            ball.bounce_x()
            ball.add_velocity(BALL_BOUNCE_VELOCITY_INCREACE)

        player1_lost = ball.rect.right < screen_rect.left
        player2_lost = ball.rect.left > screen_rect.right

        if player1_lost or player2_lost:
            ball.set_motion(
                to_rect_relitive_points(screen_rect, BALL_START_LOCATION, reverse_x=player1_lost),
                BALL_START_SLOPE, BALL_START_VELOCITY * (-1 if player1_lost else 1)
            )

        if ball.rect.top < screen_rect.top or ball.rect.bottom > screen_rect.bottom:
            ball.bounce_y()

        all_sprites.draw(screen)
        pygame.display.update()

        clock.tick(FRAMERATE)

    pygame.quit()


if __name__ == "__main__":
    main()
