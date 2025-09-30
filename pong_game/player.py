import pathlib
import sys

import pygame
import numpy as np

from ball import Ball
from utils import ScreenRelativeVector2 as RelVec2

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent))

import neural_network as nn

class Constants:
    SPEED = 3
    COLOR = "white"

class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, start_position: RelVec2, size: RelVec2) -> None:
        super().__init__()
        
        self.screen = screen

        self.start_position = start_position
        self.size = size
        
        self.score = 0
            
        self.image = pygame.Surface(self.size.to_pixels(self.screen))
        self.image.fill(Constants.COLOR)
        
        self.rect = self.image.get_rect()
                
        self.rect.center = self.start_position.to_pixels(self.screen)

        self.direction = 0

    def find_next_move(self, ball: Ball, screen: pygame.Surface) -> None:
        pass

    def add_score(self) -> None:
        self.score += 1
                    
    def go_up(self) -> None:
        self.rect.y -= Constants.SPEED
    
    def go_down(self) -> None:
        self.rect.y += Constants.SPEED
    
    def update(self) -> None:

        self.image = pygame.Surface(self.size.to_pixels(self.screen))
        self.image.fill(Constants.COLOR)

        self.rect.centerx = self.start_position.to_pixels(self.screen).x
        self.rect.clamp_ip(self.screen.get_rect())
        
        if self.direction > 0:
            self.go_up()
        elif self.direction < 0:
            self.go_down()

class HumanPaddle(Paddle):
    def __init__(self, screen: pygame.Surface, start_position: RelVec2, size: RelVec2) -> None:
        super().__init__(screen, start_position, size)
            
        if start_position.x < 0.5:
            self.up_key = pygame.K_w
            self.down_key = pygame.K_s
        else:
            self.up_key = pygame.K_UP
            self.down_key = pygame.K_DOWN
    
    def find_next_move(self, ball, screen):
        keys = pygame.key.get_pressed()
        self.direction = keys[self.up_key] - keys[self.down_key]

class BallFollowPaddle(Paddle):

    def find_next_move(self, ball: Ball, screen: pygame.Surface) -> None:
        current_y = self.rect.centery
        target_y = ball.rect.centery
        
        self.direction = current_y - target_y
    
class WallPaddle(Paddle):
    def __init__(self, screen: pygame.Surface, start_position: RelVec2, size: RelVec2) -> None:
        super().__init__(screen, start_position, RelVec2(size.x, 1.0))

class BallPredictionPaddle(Paddle):
    HISTORY_X = []
    HISTORY_Y = []

    def find_next_move(self, ball: Ball, screen: pygame.Surface) -> None:
        if ball.velocity.x == 0:
            predicted_y = ball.rect.centery
        else:
            time_to_reach_paddle = abs((self.rect.centerx - ball.rect.centerx) / ball.velocity.x)
            predicted_y = ball.rect.centery + ball.velocity.y * time_to_reach_paddle
            
            screen_height = screen.get_height()
            if predicted_y < 0:
                predicted_y = -predicted_y
            elif predicted_y > screen_height:
                predicted_y = screen_height - (predicted_y - screen_height)
            
            self.predicted_y = predicted_y

        current_y = self.rect.centery

        self.direction = current_y - predicted_y

        BallPredictionPaddle.HISTORY_X.append([self.rect.centerx, self.rect.centery, ball.rect.centerx, ball.rect.centery, ball.velocity.x, ball.velocity.y])
        BallPredictionPaddle.HISTORY_Y.append(self.direction)

class AIPaddle(Paddle):

    def __init__(self, screen: pygame.Surface, start_position: RelVec2, size: RelVec2) -> None:
        super().__init__(screen, start_position, size)

        self.model = nn.network.Network(
            [
                nn.layers.Dense(4, 6),
                nn.activations.ReLU(),
                nn.layers.Dense(6, 1),
            ],
            loss=nn.losses.MSE()
        )

    @staticmethod
    def create_inputs(paddle: Paddle, ball: Ball, screen: pygame.Surface) -> np.ndarray:
        return np.array([
            paddle.rect.centerx / screen.get_width(),
            paddle.rect.centery / screen.get_height(),
            ball.rect.centerx / screen.get_width(),
            ball.rect.centery / screen.get_height(),
            ball.x_velocity / ball.max_velocity,
            ball.y_velocity / ball.max_velocity,
        ]).reshape(-1, 6)

    def find_next_move(self, ball: Ball, screen: pygame.Surface) -> None:
        pass