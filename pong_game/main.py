import pygame
from ball import Ball
from player import HumanPaddle, AiPaddle, WallPaddle
from utils import to_rect_relitive_points, rect_centered_point, reverse_point


def make_screen_size(size_px: int, aspect_ration: float, horizontal: bool = True) -> tuple[int, int]:
    return int(size_px * ((aspect_ration * (horizontal)) or 1)), int(size_px * ((aspect_ration * (not horizontal)) or 1))


class GameConstants:
    BACKGROUND_COLOR = "black"
    EXTRA_ITEM_COLOR = "white"
    
    WINDOW_NAME = "Pong Game"
    FRAMERATE = 60

    SCORE_TO_WIN = 10

    SCORE_LOCATION = 0.45, 0.05

    LINE_LOCATION = 0.5, 1


class BallConstants:
    SIZE = 10
    
    START_VELOCITY = 2
    MAX_VELOCITY = 6

    START_LOCATION = 0.07, 0.1
    START_SLOPE = 1, 2
    BOUNCE_VELOCITY_INCREACE = 0.1


class PaddleConstants:
    START_LOCATION = 0.06, 0.5
    PADDLE_SIZE = 0.005, 0.1
    
    TOP_AREA_SIZE = 1


def main() -> None:
    pygame.init()
    
    screen = pygame.display.set_mode(
        make_screen_size(size_px=400, aspect_ration=16/10, horizontal=True)
    )
    pygame.display.set_caption(GameConstants.WINDOW_NAME)

    screen_rect = screen.get_rect()

    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 32)

    ball = Ball(
        BallConstants.SIZE, to_rect_relitive_points(screen_rect, BallConstants.START_LOCATION),
        BallConstants.START_SLOPE, BallConstants.START_VELOCITY,  BallConstants.MAX_VELOCITY
    )

    left_player = HumanPaddle(
        to_rect_relitive_points(screen_rect, PaddleConstants.START_LOCATION, reverse_x=False),
        to_rect_relitive_points(screen_rect, PaddleConstants.PADDLE_SIZE),
        pygame.K_q, pygame.K_a
    )

    right_player = HumanPaddle(
        to_rect_relitive_points(screen_rect, PaddleConstants.START_LOCATION, reverse_x=True),
        to_rect_relitive_points(screen_rect, PaddleConstants.PADDLE_SIZE),
        pygame.K_p, pygame.K_l
    )
    
    players = pygame.sprite.Group(left_player, right_player)  # type: ignore
    all_sprites = pygame.sprite.Group(*players, ball)  # type: ignore


    def ball_to_starting_position(to_reverse_side=False):
        ball.set_new_motion(
            to_rect_relitive_points(screen_rect, BallConstants.START_LOCATION, reverse_x=to_reverse_side),
            reverse_point(BallConstants.START_SLOPE, reverse_y=to_reverse_side)
        )

    def draw_score() -> None:
        player1_score_font = font.render(str(left_player.score), True, GameConstants.EXTRA_ITEM_COLOR)
        screen.blit(
            player1_score_font, rect_centered_point(player1_score_font.get_rect(),
            to_rect_relitive_points(screen_rect, GameConstants.SCORE_LOCATION, reverse_x=False))
        )

        player2_score_font = font.render(str(right_player.score), True, GameConstants.EXTRA_ITEM_COLOR)
        screen.blit(player2_score_font, rect_centered_point(
            player2_score_font.get_rect(),                             
            to_rect_relitive_points(screen_rect, GameConstants.SCORE_LOCATION, reverse_x=True))
        )
    
    while not pygame.event.get(pygame.QUIT):
        screen.fill(GameConstants.BACKGROUND_COLOR)
        pygame.draw.line(screen, GameConstants.EXTRA_ITEM_COLOR,
                to_rect_relitive_points(screen_rect, GameConstants.LINE_LOCATION),
                to_rect_relitive_points(screen_rect, GameConstants.LINE_LOCATION, reverse_y=True))

        all_sprites.update()
        
        left_player.rect.clamp_ip(screen_rect) 
        right_player.rect.clamp_ip(screen_rect) 


        collisions = collision_paddle = pygame.sprite.spritecollide(ball, players, False)
        if collisions:
            collision_paddle = collisions[0].rect
            if abs(ball.rect.right - collision_paddle.left) < ball.max_velocity or abs(ball.rect.left - collision_paddle.right) < ball.max_velocity:
                ball.bounce_x()
            if abs(ball.rect.top - collision_paddle.bottom) < ball.max_velocity or abs(ball.rect.bottom - collision_paddle.top) < ball.max_velocity:
                ball.bounce_y()

            ball.add_velocity(BallConstants.BOUNCE_VELOCITY_INCREACE)
        
        if ball.rect.right < screen_rect.left:
            # ball went over left side of wall
            ball_to_starting_position(to_reverse_side=True)
            right_player.add_score()
        
        elif ball.rect.left > screen_rect.right:
            # ball went over right side of wall
            ball_to_starting_position(to_reverse_side=False)
            left_player.add_score()     

        if ball.rect.top < screen_rect.top or ball.rect.bottom > screen_rect.bottom:
            # ball hit top or buttom
            ball.bounce_y()

        draw_score()

        all_sprites.draw(screen)
        pygame.display.update()

        clock.tick(GameConstants.FRAMERATE)

if __name__ == "__main__":
    main()
