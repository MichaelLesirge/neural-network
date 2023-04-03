import pygame
from ball import Ball
from player import HumanPaddle, AiPaddle, WallPaddle
from utils import to_rect_relitive_points, rect_centered_point


def make_screen_size(size_px: int, aspect_ration: float, horizontal: bool = True):
    return int(size_px * ((aspect_ration * (horizontal)) or 1)), int(size_px * ((aspect_ration * (not horizontal)) or 1))

# def does_ball_collide(ball: , paddle: pygame.rect.Rect)

class GameConstants:
    WINDOW_NAME = "Pong Game"
    FRAMERATE = 60

    SCORE_TO_WIN = 10
    
    SCORE_LOCATION = 0.45, 0.05
    
    LINE_LOCATION = 0.5, 1

class BallConstants:
    SIZE = 10
    MAX_VELOCITY = 6

    START_LOCATION = 0.07, 0.1
    START_SLOPE = 2 / 1
    START_VELOCITY = 2
    BOUNCE_VELOCITY_INCREACE = 0.1

class PaddleConstants:
    START_LOCATION = 0.06, 0.5
    PADDLE_SIZE = 0.01, 0.2


def main():
    pygame.init()
    pygame.display.set_caption(GameConstants.WINDOW_NAME)

    screen = pygame.display.set_mode(
        make_screen_size(size_px=400, aspect_ration=16/10, horizontal=True)
    )
    
    screen_rect = screen.get_rect()

    clock = pygame.time.Clock()
    
    font = pygame.font.Font('freesansbold.ttf', 32)

    ball = Ball(
        BallConstants.SIZE, to_rect_relitive_points(screen_rect, BallConstants.START_LOCATION),
        BallConstants.START_SLOPE, BallConstants.START_VELOCITY, BallConstants.MAX_VELOCITY
    )

    player1 = HumanPaddle(
        to_rect_relitive_points(screen_rect, PaddleConstants.START_LOCATION, reverse_x=False),
        to_rect_relitive_points(screen_rect, PaddleConstants.PADDLE_SIZE),
        pygame.K_q, pygame.K_a
    )

    player2 = HumanPaddle(
        to_rect_relitive_points(screen_rect, PaddleConstants.START_LOCATION, reverse_x=True),
        to_rect_relitive_points(screen_rect, PaddleConstants.PADDLE_SIZE),
        pygame.K_p, pygame.K_l
    )

    all_sprites = pygame.sprite.Group(ball, player1, player2)  # type: ignore

    running = True
    while running:
        screen.fill("black")
        pygame.draw.line(screen, "white",
                        to_rect_relitive_points(screen_rect, GameConstants.LINE_LOCATION),
                        to_rect_relitive_points(screen_rect, GameConstants.LINE_LOCATION, reverse_y=True))

        if pygame.event.get(pygame.QUIT):
            running = False

        all_sprites.update()

        # prevent paddles from leaving screen
        player1.rect.clamp_ip(screen_rect)
        player2.rect.clamp_ip(screen_rect)

        if ball.rect.collideobjects((player1.rect, player2.rect)):
            # ball hit a paddle
            ball.bounce_x()
            ball.add_velocity(BallConstants.BOUNCE_VELOCITY_INCREACE)

        elif ball.rect.right < screen_rect.left:
            # Went over the left side of screen, player 2 wins
            ball.set_motion(
                to_rect_relitive_points(screen_rect, BallConstants.START_LOCATION, reverse_x=True),
                BallConstants.START_SLOPE, BallConstants.START_VELOCITY
            )
            ball.bounce_x()
            player2.add_score()
            
        elif ball.rect.left > screen_rect.right:
            # Went over the right side of screen, player 1 wins
            ball.set_motion(
                to_rect_relitive_points(screen_rect, BallConstants.START_LOCATION, reverse_x=False),
                BallConstants.START_SLOPE, BallConstants.START_VELOCITY
            )
            player1.add_score()
        
        if ball.rect.top < screen_rect.top or ball.rect.bottom > screen_rect.bottom:
            # Hit top or buttom
            ball.bounce_y()
            
        player1_score_font = font.render(str(player1.score), True, "white")
        screen.blit(player1_score_font, rect_centered_point(player1_score_font.get_rect(), to_rect_relitive_points(screen_rect, GameConstants.SCORE_LOCATION, reverse_x=False)))
        
        player2_score_font = font.render(str(player2.score), True, "white")
        screen.blit(player2_score_font, rect_centered_point(player2_score_font.get_rect(), to_rect_relitive_points(screen_rect, GameConstants.SCORE_LOCATION, reverse_x=True)))

        all_sprites.draw(screen)
        pygame.display.update() 

        clock.tick(GameConstants.FRAMERATE)

    pygame.quit()


if __name__ == "__main__":
    main()
