import random

import pygame

from ball import Ball
from player import Paddle, BallFollowPaddle, HumanPaddle, WallPaddle, BallPredictionPaddle, AIPaddle
from choose import Chooser
from button import Button
from utils import ScreenRelativeVector2 as RelVec2

def make_screen_size(size_px: int, aspect_ration: float) -> tuple[int, int]:
    return int(size_px * aspect_ration), int(size_px)

class GameConstants:
    BACKGROUND_COLOR = "black"
    MAP_ITEM_COLOR = "white"
    
    WINDOW_NAME = "Pong Game"
    WINDOW_SIZE = make_screen_size(size_px=600, aspect_ration=(1+5**0.5)/2)
    FRAMERATE = 60

    SCORE_TO_WIN = 10

    SCORE_LOCATION = RelVec2(0.45, 0.05)

class BallConstants:
    SIZE = 10
    
    START_LOCATION = RelVec2(0.07, 0.1)
    START_VELOCITY = RelVec2(2, 1).normalize() * 0.005
    MAX_VELOCITY = 0.02

    BOUNCE_SPEED_COEFFICIENT = 1.02

class PaddleConstants:
    PADDLE_PERCENTAGE_OF_SCREEN = 15

    START_LOCATION = RelVec2(0.06, 0.5)
    PADDLE_SIZE = RelVec2(0.005, PADDLE_PERCENTAGE_OF_SCREEN / 100)
    
class MenuConstants:
    START_BUTTON_LOCATION = RelVec2(0.5, 0.8)
    OPTIONS_LOCATION = RelVec2(0.25, 0.2)
    BUTTON_SIZE = RelVec2(0.3, 0.1)
    MENU_BUTTON_SIZE = RelVec2(0.4, 0.1)

    SCORE_LOCATION = RelVec2(0.45, 0.05)
    VERSUS_LOCATION = RelVec2(0.5, 0.4)

def simple_bounce_angle(ball: Ball, paddle: Paddle) -> float:
    start_angle = ball.velocity.as_polar()[1]
    return 180 - start_angle

def advanced_bounce_angle(ball: Ball, paddle: Paddle) -> float:
    bounce_location = (ball.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
    return (180 if ball.velocity.x > 0 else 0) + bounce_location * 75

BOUNCE_ANGLE_FUNCTION = simple_bounce_angle

def main() -> None:

    # Initialization
    pygame.init()

    pygame.display.set_caption(GameConstants.WINDOW_NAME)
    screen = pygame.display.set_mode(
        GameConstants.WINDOW_SIZE,
        flags = pygame.RESIZABLE
    )

    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 32)

    # Menu elements
    start_game_button = Button(screen, "Start Game", MenuConstants.START_BUTTON_LOCATION, MenuConstants.MENU_BUTTON_SIZE)
    quit_game_button = Button(screen, "Quit Game", MenuConstants.START_BUTTON_LOCATION + RelVec2(0, -0.15), MenuConstants.MENU_BUTTON_SIZE)

    def create_players(left_side: bool) -> list[Paddle]:
        start_location = PaddleConstants.START_LOCATION if left_side else PaddleConstants.START_LOCATION.mirrored()
        size = PaddleConstants.PADDLE_SIZE
        
        return [
            HumanPaddle(screen, start_location, size, pygame.K_w if left_side else pygame.K_UP, pygame.K_s if left_side else pygame.K_DOWN),
            WallPaddle(screen, start_location, size),
            # BallFollowPaddle(screen, start_location, size),
            # BallPredictionPaddle(screen, start_location, size),
            AIPaddle(screen, start_location, size, AIPaddle.DEFAULT_NETWORK),
            AIPaddle(screen, start_location, size, AIPaddle.SMALL_NETWORK),
        ]

    left_players = create_players(left_side=True)
    right_players = create_players(left_side=False)

    left_buttons = [
        Button(screen, player, MenuConstants.OPTIONS_LOCATION + RelVec2(0, i * (MenuConstants.BUTTON_SIZE.y + 0.05)), MenuConstants.BUTTON_SIZE)
        for i, player in enumerate(left_players)
    ]

    right_buttons = [
        Button(screen, player, MenuConstants.OPTIONS_LOCATION.mirrored() + RelVec2(0, i * (MenuConstants.BUTTON_SIZE.y + 0.05)), MenuConstants.BUTTON_SIZE)
        for i, player in enumerate(right_players)
    ]

    left_player_chooser = Chooser(left_buttons)
    right_player_chooser = Chooser(right_buttons, default_enabled=2)

    overlay_toggle_button = Button(screen, "Overlays", RelVec2(0.5, 0.95), RelVec2(0.1, 0.05), outline_size=1)

    menu_buttons = pygame.sprite.Group(
        *left_buttons,
        *right_buttons,
        start_game_button,
        overlay_toggle_button,
    )

    # Game elements
    left_player = WallPaddle(screen, PaddleConstants.START_LOCATION, PaddleConstants.PADDLE_SIZE)
    right_player = WallPaddle(screen, PaddleConstants.START_LOCATION.mirrored(), PaddleConstants.PADDLE_SIZE)

    player_group = pygame.sprite.Group(left_player, right_player)
    
    ball = Ball(screen, BallConstants.SIZE)
    ball_group = pygame.sprite.GroupSingle(ball)
    
    ball.set_position(BallConstants.START_LOCATION)
    ball.set_velocity(BallConstants.START_VELOCITY)

    # Main loop

    has_game_started = False
    has_game_finished = False

    game_paused = False

    last_collision_paddle: Paddle | None = None

    going = True

    while going:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game_button.set(True)
                elif event.key == pygame.K_ESCAPE and has_game_started and not has_game_finished:
                    game_paused = not game_paused
                    start_game_button.set(not game_paused)
                    if game_paused:
                        print("Game Paused")
                        menu_buttons.add(start_game_button, quit_game_button)
                        start_game_button.set_object("Resume Game")
                    else:
                        print("Game Resumed")
                        menu_buttons.empty()
                if event.key == pygame.K_TAB:
                    overlay_toggle_button.set(not overlay_toggle_button.get())

        screen.fill(GameConstants.BACKGROUND_COLOR)
    
        if overlay_toggle_button.get():
            left_player.draw_overlay(screen)
            right_player.draw_overlay(screen)

        pygame.draw.line(screen, GameConstants.MAP_ITEM_COLOR, 
            (screen.get_rect().centerx, 0), 
            (screen.get_rect().centerx, screen.get_rect().bottom), 
            width=3
        )
        
        if not has_game_started and not has_game_finished:
            versus_text = font.render("VS", True, GameConstants.MAP_ITEM_COLOR, GameConstants.BACKGROUND_COLOR)
            screen.blit(versus_text, versus_text.get_rect(center=MenuConstants.VERSUS_LOCATION.to_pixels(screen)))

        if has_game_finished:
            win_text = "Left Player Wins!" if left_player.score >= GameConstants.SCORE_TO_WIN else "Right Player Wins!"
            win_font = font.render(win_text, True, GameConstants.MAP_ITEM_COLOR, GameConstants.BACKGROUND_COLOR)
            screen.blit(win_font, win_font.get_rect(center=RelVec2(0.5, 0.3).to_pixels(screen)))

        if start_game_button.get() and not has_game_started:
            print("Game Started")
            menu_buttons.empty()
            player_group.empty()

            left_player = left_player_chooser.get()
            right_player = right_player_chooser.get()

            print(f"Left Player: {left_player.get_description()}")
            print(f"Right Player: {right_player.get_description()}")

            player_group.add(left_player, right_player)
            ball_group.add(ball)

            left_player.reset_score()
            right_player.reset_score()

            ball.set_position(BallConstants.START_LOCATION)
            ball.set_velocity(BallConstants.START_VELOCITY)

            has_game_started = True
            has_game_finished = False

            menu_buttons.add(overlay_toggle_button)

        if start_game_button.get() and game_paused:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))

        if quit_game_button.get():
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        menu_buttons.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])

        if not game_paused:
            player_group.update()
            ball_group.update()

        if any(button.is_hovered for button in menu_buttons):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        left_player.find_next_move(ball)
        right_player.find_next_move(ball)

        collisions = pygame.sprite.spritecollide(ball, player_group, False)

        if collisions:
            collision_paddle: Paddle = collisions[0]

            if collision_paddle is not last_collision_paddle:
                new_velocity_magnitude = min(ball.velocity.magnitude() * BallConstants.BOUNCE_SPEED_COEFFICIENT, BallConstants.MAX_VELOCITY)
                new_velocity_angle = BOUNCE_ANGLE_FUNCTION(ball, collision_paddle)
                ball.set_velocity(RelVec2.from_polar((new_velocity_magnitude, new_velocity_angle)))

            last_collision_paddle = collision_paddle
        
        if ball.rect.right < screen.get_rect().left and has_game_started:
            # ball went over left side of wall
            ball.set_position(BallConstants.START_LOCATION)
            ball.set_velocity(BallConstants.START_VELOCITY + RelVec2(random.random(), random.random()) / 1000)
            right_player.add_score()
            last_collision_paddle = None
            print("Right Player Scored")
        
        elif ball.rect.left > screen.get_rect().right and has_game_started:
            # ball went over right side of wall
            ball.set_position(BallConstants.START_LOCATION.mirrored())
            ball.set_velocity((BallConstants.START_VELOCITY + RelVec2(random.random(), random.random()) / 1000).mirrored_velocity())
            left_player.add_score()
            last_collision_paddle = None
            print("Left Player Scored")

        if ball.rect.top < screen.get_rect().top or ball.rect.bottom > screen.get_rect().bottom:
            # ball hit top or bottom
            ball.bounce_y()

        if (left_player.score >= GameConstants.SCORE_TO_WIN or right_player.score >= GameConstants.SCORE_TO_WIN) and not has_game_finished:
            print("Game Finished")

            has_game_finished = True
            has_game_started = False

            ball_group.empty()

            ball.set_velocity(RelVec2(0, 0))
            ball.set_position(RelVec2(0.5, 0.5))

            start_game_button.set(False)
            start_game_button.set_object("Play Again?")

            menu_buttons.add(start_game_button, quit_game_button)

        left_player_score_font = font.render(str(left_player.score), True, GameConstants.MAP_ITEM_COLOR)
        right_player_score_font = font.render(str(right_player.score), True, GameConstants.MAP_ITEM_COLOR)

        screen.blit(left_player_score_font, left_player_score_font.get_rect(center=MenuConstants.SCORE_LOCATION.to_pixels(screen)))
        screen.blit(right_player_score_font, right_player_score_font.get_rect(center=MenuConstants.SCORE_LOCATION.mirrored().to_pixels(screen)))

        player_group.draw(screen)
        ball_group.draw(screen)
        menu_buttons.draw(screen)

        pygame.display.update()

        clock.tick(GameConstants.FRAMERATE)
    
if __name__ == "__main__":
    main()
