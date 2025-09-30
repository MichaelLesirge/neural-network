import pygame


from ball import Ball
from player import Paddle, BallFollowPaddle, HumanPaddle, WallPaddle, BallPredictionPaddle
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
    START_LOCATION = RelVec2(0.06, 0.5)
    PADDLE_SIZE = RelVec2(0.005, 0.15)
    
class MenuConstants:
    START_BUTTON_LOCATION = RelVec2(0.5, 0.8)
    OPTIONS_LOCATION = RelVec2(0.25, 0.2)
    BUTTON_SIZE = RelVec2(0.3, 0.1)

    SCORE_LOCATION = RelVec2(0.45, 0.05)
    VERSUS_LOCATION = RelVec2(0.5, 0.4)

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
    start_game_button = Button(screen, "Start Game", MenuConstants.START_BUTTON_LOCATION, MenuConstants.BUTTON_SIZE)

    left_players = {
        "WASD": HumanPaddle(screen, PaddleConstants.START_LOCATION, PaddleConstants.PADDLE_SIZE, pygame.K_w, pygame.K_s),
        "Wall": WallPaddle(screen, PaddleConstants.START_LOCATION, PaddleConstants.PADDLE_SIZE),
        "Follower": BallFollowPaddle(screen, PaddleConstants.START_LOCATION, PaddleConstants.PADDLE_SIZE),
        "Predictor": BallPredictionPaddle(screen, PaddleConstants.START_LOCATION, PaddleConstants.PADDLE_SIZE),
    }

    right_players = {
        "Arrows": HumanPaddle(screen, PaddleConstants.START_LOCATION.mirrored(), PaddleConstants.PADDLE_SIZE, pygame.K_UP, pygame.K_DOWN),
        "Wall": WallPaddle(screen, PaddleConstants.START_LOCATION.mirrored(), PaddleConstants.PADDLE_SIZE),
        "Follower": BallFollowPaddle(screen, PaddleConstants.START_LOCATION.mirrored(), PaddleConstants.PADDLE_SIZE),
        "Predictor": BallPredictionPaddle(screen, PaddleConstants.START_LOCATION.mirrored(), PaddleConstants.PADDLE_SIZE),
    }

    left_buttons = [
        Button(screen, name, MenuConstants.OPTIONS_LOCATION + RelVec2(0, i * (MenuConstants.BUTTON_SIZE.y + 0.05)), MenuConstants.BUTTON_SIZE)
        for i, name in enumerate(left_players.keys())
    ]

    right_buttons = [
        Button(screen, name, MenuConstants.OPTIONS_LOCATION.mirrored() + RelVec2(0, i * (MenuConstants.BUTTON_SIZE.y + 0.05)), MenuConstants.BUTTON_SIZE)
        for i, name in enumerate(right_players.keys())
    ]

    left_player_chooser = Chooser(left_buttons)
    right_player_chooser = Chooser(right_buttons)

    menu_buttons = pygame.sprite.Group(
        *left_buttons,
        *right_buttons,
        start_game_button
    )

    # Game elements
    left_player = left_players["Wall"]
    right_player = right_players["Wall"]

    player_group = pygame.sprite.Group(left_player, right_player)
    
    ball = Ball(screen, BallConstants.SIZE, BallConstants.MAX_VELOCITY)
    ball_group = pygame.sprite.GroupSingle(ball)

    # Main loop

    has_game_started = False

    ball.set_position(BallConstants.START_LOCATION)
    ball.set_velocity(BallConstants.START_VELOCITY)

    while not pygame.event.get(pygame.QUIT):
        
        screen.fill(GameConstants.BACKGROUND_COLOR)
    
        pygame.draw.line(screen, GameConstants.MAP_ITEM_COLOR, 
            (screen.get_rect().centerx, 0), 
            (screen.get_rect().centerx, screen.get_rect().bottom), 
            width=3
        )
        
        if not start_game_button.get():
            versus_text = font.render("VS", True, GameConstants.MAP_ITEM_COLOR, GameConstants.BACKGROUND_COLOR)
            screen.blit(versus_text, versus_text.get_rect(center=MenuConstants.VERSUS_LOCATION.to_pixels(screen)))
        
        menu_buttons.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
        player_group.update()
        ball_group.update()

        left_player.find_next_move(ball, screen)
        right_player.find_next_move(ball, screen)

        if start_game_button.get() and not has_game_started:
            menu_buttons.empty()

            left_player = left_players[left_player_chooser.get()]
            right_player = right_players[right_player_chooser.get()]

            player_group = pygame.sprite.Group(left_player, right_player)

            ball.set_position(BallConstants.START_LOCATION)
            ball.set_velocity(BallConstants.START_VELOCITY)

            has_game_started = True

        collisions = pygame.sprite.spritecollide(ball, player_group, False)

        if collisions:
            collision_paddle = collisions[0].rect
            ball_velocity_pixel = (ball.velocity.normalize() * ball.max_velocity).to_pixels(screen).magnitude()
            if abs(ball.rect.right - collision_paddle.left) < ball_velocity_pixel or abs(ball.rect.left - collision_paddle.right) < ball_velocity_pixel:
                ball.bounce_x()
            if abs(ball.rect.top - collision_paddle.bottom) < ball_velocity_pixel or abs(ball.rect.bottom - collision_paddle.top) < ball_velocity_pixel:
                ball.bounce_y()

            ball.velocity_times(BallConstants.BOUNCE_SPEED_COEFFICIENT)
        
        if ball.rect.right < screen.get_rect().left:
            # ball went over left side of wall
            ball.set_position(BallConstants.START_LOCATION)
            ball.set_velocity(BallConstants.START_VELOCITY)
            right_player.add_score()
        
        elif ball.rect.left > screen.get_rect().right:
            # ball went over right side of wall
            ball.set_position(BallConstants.START_LOCATION.mirrored())
            ball.set_velocity(pygame.Vector2(-BallConstants.START_VELOCITY.x, BallConstants.START_VELOCITY.y))
            left_player.add_score()

        if ball.rect.top < screen.get_rect().top or ball.rect.bottom > screen.get_rect().bottom:
            # ball hit top or bottom
            ball.bounce_y()

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
