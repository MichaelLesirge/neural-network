from time import sleep

import pygame

from ball import Ball
from player import AiPaddle, HumanPaddle, WallPaddle
from utils import RelativeRectPoint


def make_screen_size(size_px: int, aspect_ration: float, horizontal: bool = True) -> tuple[int, int]:
    return int(size_px * ((aspect_ration * (horizontal)) or 1)), int(size_px * ((aspect_ration * (not horizontal)) or 1))


class GameConstants:
    BACKGROUND_COLOR = "black"
    MAP_ITEM_COLOR = "white"
    
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
    BOUNCE_VELOCITY_INCREASE = 0.1


class PaddleConstants:
    START_LOCATION = 0.06, 0.5
    PADDLE_SIZE = 0.005, 0.15
    
    TOP_AREA_SIZE = 1


def main() -> None:
    pygame.init()
    
    screen = pygame.display.set_mode(
        make_screen_size(size_px=400, aspect_ration=16/10, horizontal=True), 
        flags = pygame.RESIZABLE
    )
    pygame.display.set_caption(GameConstants.WINDOW_NAME)

    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 32)

    ball = Ball(
        BallConstants.SIZE, RelativeRectPoint(screen, BallConstants.START_LOCATION),
        BallConstants.START_SLOPE, BallConstants.START_VELOCITY,  BallConstants.MAX_VELOCITY
    )

    left_player = HumanPaddle(
        RelativeRectPoint(screen, PaddleConstants.START_LOCATION, reverse_x=False),
        RelativeRectPoint(screen, PaddleConstants.PADDLE_SIZE),
        pygame.K_q, pygame.K_a
    )

    right_player = HumanPaddle(
        RelativeRectPoint(screen, PaddleConstants.START_LOCATION, reverse_x=True),
        RelativeRectPoint(screen, PaddleConstants.PADDLE_SIZE),
        pygame.K_p, pygame.K_l
    )
    
    players = pygame.sprite.Group([left_player, right_player])  # type: ignore
    
    all_sprites = pygame.sprite.Group([*players, ball])  # type: ignore

    def draw_score() -> None:
        left_player_score_font = font.render(str(left_player.score), True, GameConstants.MAP_ITEM_COLOR)
        screen.blit(
            left_player_score_font,
            RelativeRectPoint(screen, GameConstants.SCORE_LOCATION, reverse_x=False).point_centered_for(left_player_score_font)
        )
        
        right_player_score_font = font.render(str(right_player.score), True, GameConstants.MAP_ITEM_COLOR)
        screen.blit(
            right_player_score_font,
            RelativeRectPoint(screen, GameConstants.SCORE_LOCATION, reverse_x=True).point_centered_for(right_player_score_font)
        )
    
    while not pygame.event.get(pygame.QUIT):
        screen.fill(GameConstants.BACKGROUND_COLOR)
        pygame.draw.line(screen, GameConstants.MAP_ITEM_COLOR,
                RelativeRectPoint(screen, GameConstants.LINE_LOCATION, reverse_y=False).point,
                RelativeRectPoint(screen, GameConstants.LINE_LOCATION, reverse_y=True).point)
        

        all_sprites.update()
         
        for player in players:
            player.rect.clamp_ip(screen.get_rect()) 
        
        if isinstance(left_player, AiPaddle):
            left_player.update_network(ball, screen, left_player.image.get_rect())
            
        if isinstance(right_player, AiPaddle):
            right_player.update_network(ball, screen, left_player.image.get_rect())

        collisions = pygame.sprite.spritecollide(ball, players, False)
        if collisions:
            collision_paddle = collisions[0].rect
            if abs(ball.rect.right - collision_paddle.left) < ball.max_velocity or abs(ball.rect.left - collision_paddle.right) < ball.max_velocity:
                ball.bounce_x()
            if abs(ball.rect.top - collision_paddle.bottom) < ball.max_velocity or abs(ball.rect.bottom - collision_paddle.top) < ball.max_velocity:
                ball.bounce_y()

            ball.add_velocity(BallConstants.BOUNCE_VELOCITY_INCREASE)
        
        if ball.rect.right < screen.get_rect().left:
            # ball went over left side of wall
            ball.to_starting_position(to_reverse_side=True)
            right_player.add_score()
        
        elif ball.rect.left > screen.get_rect().right:
            # ball went over right side of wall
            ball.to_starting_position(to_reverse_side=False)
            left_player.add_score()     

        if ball.rect.top < screen.get_rect().top or ball.rect.bottom > screen.get_rect().bottom:
            # ball hit top or bottom
            ball.bounce_y()

        draw_score()

        all_sprites.draw(screen)
        pygame.display.update()

        clock.tick(GameConstants.FRAMERATE)

if __name__ == "__main__":
    main()
