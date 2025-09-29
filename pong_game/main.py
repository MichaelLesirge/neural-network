from time import sleep

import pygame

from ball import Ball
from player import Paddle, BallFollowPaddle, HumanPaddle, WallPaddle
from utils import RPoint
from choose import Chooser
from button import Button

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
    
    START_VELOCITY = 4
    MAX_VELOCITY = 12

    START_LOCATION = 0.07, 0.1
    START_SLOPE = 0.5, 1
    BOUNCE_VELOCITY_INCREASE = 0.25


class PaddleConstants:
    START_LOCATION = 0.06, 0.5
    PADDLE_SIZE = 0.005, 0.15
    
    TOP_AREA_SIZE = 1

class MenuConstants:
    START_BUTTON_LOCATION = 0.5, 0.7

    OPTIONS_LOCATION = 0.25, 0.2

    BUTTON_SIZE = 0.3, 0.1
    BUTTON_GAP = 0.05

LEFT_PLAYER_TYPES = {
    "Human": lambda screen: HumanPaddle(
        RPoint(screen, PaddleConstants.START_LOCATION, reverse_x=False),
        RPoint(screen, PaddleConstants.PADDLE_SIZE),
        pygame.K_q, pygame.K_a
    ),
    "Simple AI": lambda screen: BallFollowPaddle(
        RPoint(screen, PaddleConstants.START_LOCATION, reverse_x=False),
        RPoint(screen, PaddleConstants.PADDLE_SIZE),
    ),
    "Wall": lambda screen: WallPaddle(
        RPoint(screen, PaddleConstants.START_LOCATION, reverse_x=False),
        RPoint(screen, PaddleConstants.PADDLE_SIZE),
    ),
}

RIGHT_PLAYER_TYPES = {
    "Human": lambda screen: HumanPaddle(
        RPoint(screen, PaddleConstants.START_LOCATION, reverse_x=True),
        RPoint(screen, PaddleConstants.PADDLE_SIZE),
        pygame.K_p, pygame.K_l
    ),
    "Simple AI": lambda screen: BallFollowPaddle(
        RPoint(screen, PaddleConstants.START_LOCATION, reverse_x=True),
        RPoint(screen, PaddleConstants.PADDLE_SIZE),
    ),
    "Wall": lambda screen: WallPaddle(
        RPoint(screen, PaddleConstants.START_LOCATION, reverse_x=True),
        RPoint(screen, PaddleConstants.PADDLE_SIZE),
    ),
}

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(
        make_screen_size(size_px=400, aspect_ration=16/10, horizontal=True), 
        flags = pygame.RESIZABLE
    )
    pygame.display.set_caption(GameConstants.WINDOW_NAME)

    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 32)

    start_game_button = Button("Start Game", RPoint(screen, MenuConstants.START_BUTTON_LOCATION), RPoint(screen, MenuConstants.BUTTON_SIZE))
    start_game_button_group = pygame.sprite.GroupSingle(start_game_button)

    left_player_chooser = Chooser(screen, LEFT_PLAYER_TYPES.keys(), RPoint(screen, MenuConstants.OPTIONS_LOCATION, reverse_x=False), RPoint(screen, MenuConstants.BUTTON_SIZE), MenuConstants.BUTTON_GAP)
    right_player_chooser = Chooser(screen, RIGHT_PLAYER_TYPES.keys(), RPoint(screen, MenuConstants.OPTIONS_LOCATION, reverse_x=True), RPoint(screen, MenuConstants.BUTTON_SIZE), MenuConstants.BUTTON_GAP)

    menu_elements = (start_game_button_group, left_player_chooser, right_player_chooser)

    menu_screen_player_type = "Wall"

    left_player: Paddle = RIGHT_PLAYER_TYPES[menu_screen_player_type](screen)
    right_player: Paddle = LEFT_PLAYER_TYPES[menu_screen_player_type](screen)

    paddle_group = pygame.sprite.Group(left_player, right_player)
    
    ball = Ball(
        BallConstants.SIZE, RPoint(screen, BallConstants.START_LOCATION),
        BallConstants.START_SLOPE, BallConstants.START_VELOCITY,  BallConstants.MAX_VELOCITY
    )
    ball_group = pygame.sprite.GroupSingle(ball)

    has_game_started = False

    while not pygame.event.get(pygame.QUIT):
        
        screen.fill(GameConstants.BACKGROUND_COLOR)
    
        pygame.draw.line(screen, GameConstants.MAP_ITEM_COLOR,
                RPoint(screen, GameConstants.LINE_LOCATION, reverse_y=False).point,
                RPoint(screen, GameConstants.LINE_LOCATION, reverse_y=True).point)
        
        if not start_game_button.get():
            versus_text = font.render("VS", True, GameConstants.MAP_ITEM_COLOR, GameConstants.BACKGROUND_COLOR)
            screen.blit(versus_text, versus_text.get_rect(center=RPoint(screen, (0.5, 0.4)).point))
        
        paddle_group.update()
        ball_group.update()

        if start_game_button.get() and not has_game_started:
            menu_elements = ()
            left_player = LEFT_PLAYER_TYPES[left_player_chooser.get()](screen)
            right_player = RIGHT_PLAYER_TYPES[right_player_chooser.get()](screen)
            paddle_group = pygame.sprite.Group(left_player, right_player)
            has_game_started = True

        for element in menu_elements:
            element.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
         
        for player in paddle_group:
            player.rect.clamp_ip(screen.get_rect()) 
        
        left_player.find_next_move(ball, screen)
        right_player.find_next_move(ball, screen)

        collisions = pygame.sprite.spritecollide(ball, paddle_group, False)
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

        left_player_score_font = font.render(str(left_player.score), True, GameConstants.MAP_ITEM_COLOR)
        screen.blit(
            left_player_score_font,
            RPoint(screen, GameConstants.SCORE_LOCATION, reverse_x=False).point_centered_for(left_player_score_font)
        )
        
        right_player_score_font = font.render(str(right_player.score), True, GameConstants.MAP_ITEM_COLOR)
        screen.blit(
            right_player_score_font,
            RPoint(screen, GameConstants.SCORE_LOCATION, reverse_x=True).point_centered_for(right_player_score_font)
        )

        paddle_group.draw(screen)
        ball_group.draw(screen)

        for menu_item in menu_elements:
            menu_item.draw(screen)

        pygame.display.update()

        clock.tick(GameConstants.FRAMERATE)

if __name__ == "__main__":
    main()
