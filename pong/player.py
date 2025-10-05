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

    def find_next_move(self, ball: Ball) -> None:
        pass

    def reset_score(self) -> None:
        self.score = 0

    def add_score(self) -> None:
        self.score += 1
                    
    def go_up(self) -> None:
        self.rect.y -= Constants.SPEED
    
    def go_down(self) -> None:
        self.rect.y += Constants.SPEED
    
    @property
    def position(self) -> RelVec2:
        return RelVec2.from_pixels(self.screen, self.rect.center)

    def update(self) -> None:

        self.image = pygame.Surface(self.size.to_pixels(self.screen))
        self.image.fill(Constants.COLOR)

        self.rect.centerx = self.start_position.to_pixels(self.screen).x
        self.rect.clamp_ip(self.screen.get_rect())
        
        if self.direction > 0:
            self.go_up()
        elif self.direction < 0:
            self.go_down()
        
    def get_description(self) -> str:
        return "Default Paddle"

    @staticmethod
    def inputs_to_array(paddle: "Paddle", ball: Ball) -> np.ndarray:
        return np.array([
            *paddle.position.xy,
            *ball.position.xy,
            *ball.velocity.xy
        ])

class HumanPaddle(Paddle):
    def __init__(self, screen: pygame.Surface, start_position: RelVec2, size: RelVec2, up_key: int, down_key: int) -> None:
        super().__init__(screen, start_position, size)
            
        self.up_key = up_key
        self.down_key = down_key
    
    def find_next_move(self, ball):
        keys = pygame.key.get_pressed()
        self.direction = keys[self.up_key] - keys[self.down_key]

    def get_description(self) -> str:
        return f"Player controlled paddle (up: {pygame.key.name(self.up_key).upper()}, down: {pygame.key.name(self.down_key).upper()})"

class BallFollowPaddle(Paddle):

    def find_next_move(self, ball: Ball) -> None:
        self.direction = self.position.y - ball.position.y
    
class WallPaddle(Paddle):
    def __init__(self, screen: pygame.Surface, start_position: RelVec2, size: RelVec2) -> None:
        super().__init__(screen, start_position, RelVec2(size.x, 1.0))

    def get_description(self):
        return "Wall paddle (does not move)"

class BallPredictionPaddle(Paddle):

    @staticmethod
    def determine_direction(paddle_x, paddle_y, ball_x, ball_y, ball_vx, ball_vy) -> float:
        if ball_vx == 0:
            return paddle_y - ball_y
        time_to_reach_paddle = abs((paddle_x - ball_x) / ball_vx)
        predicted_y = ball_y + ball_vy * time_to_reach_paddle
        
        predicted_y = predicted_y % 2.0
        if predicted_y > 1.0:
            predicted_y = 2.0 - predicted_y

        return paddle_y - predicted_y

    def find_next_move(self, ball: Ball) -> None:
        inputs = Paddle.inputs_to_array(self, ball)
        self.direction = BallPredictionPaddle.determine_direction(*inputs.tolist())

    def get_description(self) -> str:
        return "Ball prediction paddle (predicts where the ball will be when it reaches the paddle)"

class AIPaddle(Paddle):

    DEFAULT_NETWORK_FILE = directory / "models"
    
    X_INPUT = 6
    Y_OUTPUT = 1

    MODELS = {
        "default": nn.network.Network(
            [
                nn.layers.Dense(X_INPUT, 16),
                nn.activations.Tanh(),
                nn.layers.Dense(16, 8),
                nn.activations.Tanh(),
                nn.layers.Dense(8, Y_OUTPUT),
            ],
            loss=nn.losses.MSE()
        ),
        "small": nn.network.Network(
            [
                nn.layers.Dense(X_INPUT, 4),
                nn.activations.Tanh(),
                nn.layers.Dense(4, 4),
                nn.activations.Tanh(),
                nn.layers.Dense(4, Y_OUTPUT),
            ],
            loss=nn.losses.MSE()
        )
    }


    def __init__(self, screen: pygame.Surface, start_position: RelVec2, size: RelVec2, model_name: str = "default") -> None:
        super().__init__(screen, start_position, size)
        if model_name not in self.MODELS:
            raise ValueError(f"Model '{model_name}' not recognized. Available models: {self.MODELS}")
        
        self.model_name = model_name
        self.model = AIPaddle.MODELS[model_name]

        try:
            self.model.load(str(self.DEFAULT_NETWORK_FILE / model_name))
        except FileNotFoundError as e:
            e.add_note(f"No saved weights for '{model_name}' model found. Please train the model before using it.")
            raise e
            

    def find_next_move(self, ball: Ball) -> None:
        inputs = Paddle.inputs_to_array(self, ball)
        output = self.model.compute(inputs)
        self.direction = output[0]

    def get_description(self) -> str:
        return f"AI paddle (model: {self.model_name}, parameters {sum(layer.weights.size + layer.biases.size for layer in self.model.layers if isinstance(layer, nn.layers.Dense))})"