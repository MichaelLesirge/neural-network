import pygame
from ball import Ball
from player import HumanPaddle, AiPaddle, WallPaddle
from utils import to_rect_relitive_points, rect_centered_point, reverse_point


def make_screen_size(size_px: int, aspect_ration: float, horizontal: bool = True) -> tuple[int, int]:
    return int(size_px * ((aspect_ration * (horizontal)) or 1)), int(size_px * ((aspect_ration * (not horizontal)) or 1))


class GameConstants:
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


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(
            make_screen_size(size_px=400, aspect_ration=16/10, horizontal=True)
        )
        pygame.display.set_caption(GameConstants.WINDOW_NAME)

        self.screen_rect = self.screen.get_rect()

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.ball = Ball(
            BallConstants.SIZE, to_rect_relitive_points(self.screen_rect, BallConstants.START_LOCATION),
            BallConstants.START_SLOPE, BallConstants.START_VELOCITY,  BallConstants.MAX_VELOCITY
        )

        self.left_player = HumanPaddle(
            to_rect_relitive_points(self.screen_rect, PaddleConstants.START_LOCATION, reverse_x=False),
            to_rect_relitive_points(self.screen_rect, PaddleConstants.PADDLE_SIZE),
            pygame.K_q, pygame.K_a
        )

        self.right_player = HumanPaddle(
            to_rect_relitive_points(self.screen_rect, PaddleConstants.START_LOCATION, reverse_x=True),
            to_rect_relitive_points(self.screen_rect, PaddleConstants.PADDLE_SIZE),
            pygame.K_p, pygame.K_l
        )

        self.all_sprites = pygame.sprite.Group(self.ball, self.left_player, self.right_player)  # type: ignore

    def run(self) -> None:
        running = True
        while running:
            self.update_screen()
            if pygame.event.get(pygame.QUIT):
                running = False
        pygame.quit()

    def ball_to_starting_position(self, to_reverse_side=False):
        self.ball.set_new_motion(
            to_rect_relitive_points(self.screen_rect, BallConstants.START_LOCATION, reverse_x=to_reverse_side),
            reverse_point(BallConstants.START_SLOPE, reverse_y=to_reverse_side)
        )

    def draw_score(self) -> None:
        player1_score_font = self.font.render(str(self.left_player.score), True, "white")
        self.screen.blit(
            player1_score_font, rect_centered_point(player1_score_font.get_rect(),
            to_rect_relitive_points(self.screen_rect, GameConstants.SCORE_LOCATION, reverse_x=False))
        )

        player2_score_font = self.font.render(str(self.right_player.score), True, "white")
        self.screen.blit(player2_score_font, rect_centered_point(
            player2_score_font.get_rect(),                                                     
            to_rect_relitive_points(self.screen_rect, GameConstants.SCORE_LOCATION, reverse_x=True))
        )

    def update_screen(self) -> None:
        self.screen.fill("black")
        pygame.draw.line(self.screen, "white",
                        to_rect_relitive_points(self.screen_rect, GameConstants.LINE_LOCATION),
                        to_rect_relitive_points(self.screen_rect, GameConstants.LINE_LOCATION, reverse_y=True))

        self.all_sprites.update()

        # prevent paddles from leaving screen
        self.left_player.rect.clamp_ip(self.screen_rect)
        self.right_player.rect.clamp_ip(self.screen_rect)

        if self.ball.rect.collideobjects((self.left_player.rect, self.right_player.rect)):
            # ball hit a paddle
            self.ball.bounce_x()
            self.ball.add_velocity(BallConstants.BOUNCE_VELOCITY_INCREACE)
        
        
        elif self.ball.rect.right < self.screen_rect.left:
            # ball went over left side of wall
            self.ball_to_starting_position(to_reverse_side=True)
            self.right_player.add_score()
        
        elif self.ball.rect.left > self.screen_rect.right:
            # ball went over right side of wall
            self.ball_to_starting_position(to_reverse_side=False)
            self.left_player.add_score()

                

        if self.ball.rect.top < self.screen_rect.top or self.ball.rect.bottom > self.screen_rect.bottom:
            # ball hit top or buttom
            self.ball.bounce_y()

        self.draw_score()

        self.all_sprites.draw(self.screen)
        pygame.display.update()

        self.clock.tick(GameConstants.FRAMERATE)


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
