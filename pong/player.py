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
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.fill(Constants.COLOR)

        self.rect.centerx = self.start_position.to_pixels(self.screen).x
        self.rect.clamp_ip(self.screen.get_rect())
        
        if self.direction > 0:
            self.go_up()
        elif self.direction < 0:
            self.go_down()
        
    def get_description(self) -> str:
        return "Default Paddle"
    
    def get_name(self) -> str:
        return "Paddle"
    
    def draw_overlay(self, screen: pygame.Surface) -> None:
        pass
    
    def __str__(self):
        return self.get_name()

class HumanPaddle(Paddle):
    def __init__(self, screen: pygame.Surface, start_position: RelVec2, size: RelVec2, up_key: int, down_key: int) -> None:
        super().__init__(screen, start_position, size)
            
        self.up_key = up_key
        self.down_key = down_key

        self.up_key_name = pygame.key.name(self.up_key).upper()
        self.down_key_name = pygame.key.name(self.down_key).upper()

        self.up_key_pressed = False
        self.down_key_pressed = False
    
    def find_next_move(self, ball):
        keys = pygame.key.get_pressed()
        self.up_key_pressed = keys[self.up_key]
        self.down_key_pressed = keys[self.down_key]
        self.direction = self.up_key_pressed - self.down_key_pressed

    def get_description(self) -> str:
        return f"Player controlled paddle (up: {self.up_key_name}, down: {self.down_key_name})"
    
    def get_name(self) -> str:
        return f"{self.up_key_name.title()}/{self.down_key_name.title()} Key"
    
    def draw_overlay(self, screen: pygame.Surface) -> None:
        font = pygame.font.Font(None, 24)

        colors = ["white", "black"]
        up_text = font.render(self.up_key_name, True, colors[self.up_key_pressed], colors[not self.up_key_pressed])
        down_text = font.render(self.down_key_name, True, colors[self.down_key_pressed], colors[not self.down_key_pressed])

        up_rect = up_text.get_rect(center=(self.rect.centerx, 30))
        down_rect = down_text.get_rect(center=(self.rect.centerx, screen.get_height() - 30))

        screen.blit(up_text, up_rect)
        screen.blit(down_text, down_rect)


class BallFollowPaddle(Paddle):
    def find_next_move(self, ball: Ball) -> None:
        self.direction = self.position.y - ball.position.y

    def get_description(self) -> str:
        return "Ball follow paddle"
    
    def get_name(self) -> str:
        return "Follower"
    
class WallPaddle(Paddle):
    def __init__(self, screen: pygame.Surface, start_position: RelVec2, size: RelVec2) -> None:
        super().__init__(screen, start_position, RelVec2(size.x, 1.0))

    def get_description(self):
        return "Wall paddle (does not move)"

    def get_name(self) -> str:
        return "Wall"
    
    def draw_overlay(self, screen):
        rect = pygame.Rect(0, 0, self.rect.width * 2, self.rect.height)
        rect.center = self.rect.center
        pygame.draw.rect(screen, "red", rect)

class BallPredictionPaddle(Paddle):

    @staticmethod
    def determine_direction(paddle_x, paddle_y, ball_x, ball_y, ball_vx, ball_vy, handle_bounces: bool = True) -> float:
        if ball_vx == 0:
            return paddle_y - ball_y
        time_to_reach_paddle = abs((paddle_x - ball_x) / ball_vx)
        predicted_y = ball_y + ball_vy * time_to_reach_paddle
        
        predicted_y = predicted_y % 2.0
        if predicted_y > 1.0 and handle_bounces:
            predicted_y = 2.0 - predicted_y

        return paddle_y - predicted_y

    def find_next_move(self, ball: Ball) -> None:
        inputs = AIPaddle.inputs_to_array(self, ball)
        self.direction = BallPredictionPaddle.determine_direction(*inputs.tolist())

    def get_description(self) -> str:
        return "Ball prediction paddle (predicts where the ball will be when it reaches the paddle)"

    def get_name(self) -> str:
        return "Predictor"
    
    def draw_overlay(self, screen):
        rect = pygame.Rect(0, 0, self.rect.width * 2, self.rect.width)
        setpoint = self.position.y - self.direction
        rect.center = RelVec2(self.position.x, setpoint).to_pixels(screen)
        pygame.draw.rect(screen, "green", rect)

class AIPaddle(Paddle):
 
    X_INPUT = 6
    Y_OUTPUT = 1

    DEFAULT_NETWORK = nn.network.Network(
        [
            nn.layers.Dense(X_INPUT, 16),
            nn.activations.Tanh(),
            nn.layers.Dense(16, 8),
            nn.activations.Tanh(),
            nn.layers.Dense(8, Y_OUTPUT),
        ],
        loss=nn.losses.MSE()
    )
    
    SMALL_NETWORK = nn.network.Network(
        [
            nn.layers.Dense(X_INPUT, 4),
            nn.activations.Tanh(),
            nn.layers.Dense(4, 4),
            nn.activations.Tanh(),
            nn.layers.Dense(4, Y_OUTPUT),
        ],
        loss=nn.losses.MSE()
    )

    NETWORK_FOLDER = directory / "models"

    MODEL_SAVE_FILES = {
        DEFAULT_NETWORK: str(NETWORK_FOLDER / "default"),
        SMALL_NETWORK: str(NETWORK_FOLDER / "small"),
    }

    def __init__(self, screen: pygame.Surface, start_position: RelVec2, size: RelVec2, model: nn.network.Network = DEFAULT_NETWORK) -> None:
        super().__init__(screen, start_position, size)

        self.model = model
        self.model_file = self.MODEL_SAVE_FILES.get(model)

        if self.model_file is not None:
            self.model.load(self.model_file)
        else:
            print("Warning: Model not recognized, not loading any saved weights.")

        self.inputs = []
    
    @staticmethod
    def inputs_to_array(paddle: "Paddle", ball: Ball) -> np.ndarray:
        return np.array([   
            *paddle.position.xy,
            *ball.position.xy,
            *ball.velocity.xy
        ])
            
    def find_next_move(self, ball: Ball) -> None:
        self.inputs = [self.inputs_to_array(self, ball).reshape(1, -1)]

        for layer in self.model.layers:
            self.inputs.append(layer.forward(self.inputs[-1]))

        self.direction = self.inputs[-1][0]

    def get_description(self) -> str:
        return f"AI paddle (model: {self.model_file}, neurons: {sum(layer.weights.shape[1] for layer in self.model.layers if isinstance(layer, nn.layers.Dense))})"
    
    def get_name(self) -> str:
        neurons = sum(layer.weights.shape[1] for layer in self.model.layers if isinstance(layer, nn.layers.Dense))
        return f"{neurons} Neuron AI"
    
    def draw_network(self, screen: pygame.Surface) -> None:
        data = []
        kept_layers = []
        for input, layer in zip(self.inputs, [None] + self.model.layers, strict=True):
            if isinstance(layer, nn.layers.Dense) or layer is None:
                data.append(input[0])
                kept_layers.append(layer)

        width = len(data)
        height = max(len(layer) for layer in data)

        def get_position(i: int, j: int) -> RelVec2:
            x = (i + 1) / (width + 1)
            y = 0.5 + (j - (len(data[i]) - 1) / 2) / height
            return RelVec2(x, y)

        for i, layer in enumerate(data):
            for j, neuron in enumerate(layer):

                position = get_position(i, j).to_pixels(screen)

                for k, next_neuron in enumerate(data[i + 1] if i + 1 < len(data) else []):
                    next_position = get_position(i + 1, k).to_pixels(screen)

                    weight = abs(kept_layers[i + 1].weights[j, k] if isinstance(kept_layers[i + 1], nn.layers.Dense) else 0.0)
                    max_weight = max(kept_layers[i + 1].weights.flatten(), default=0.0) if isinstance(kept_layers[i + 1], nn.layers.Dense) else 0.0

                    normized_weight = weight / max_weight if max_weight != 0 else 0
                    line_color = (
                        100 * normized_weight,
                        100 * normized_weight,
                        100 * normized_weight
                    )

                    pygame.draw.line(screen, line_color, position, next_position, 1)

                normized_value = np.tanh(neuron)
                color = (
                    10 if normized_value > 0 else int(255 * abs(normized_value)),
                    10,
                    10 if normized_value < 0 else int(255 * abs(normized_value)),
                )
                inner_color = (
                    255 if normized_value < 0 else 0,
                    0,
                    255 if normized_value > 0 else 0,
                )

                neruon_radius = 10
                pygame.draw.circle(screen, (30, 30, 30), position, neruon_radius + 1)
                pygame.draw.circle(screen, color, position, neruon_radius)
                pygame.draw.circle(screen, inner_color, position, interplate(1, neruon_radius, abs(normized_value)))

    def draw_overlay(self, screen: pygame.Surface) -> None:
        rect = pygame.Rect(0, 0, screen.get_width() * 0.5, screen.get_height() * 0.8)
        flipped = self.rect.centerx > screen.get_width() / 2
        rect.center = (screen.get_width() * (0.75 if flipped else 0.25), screen.get_height() * 0.5)

        newwork_surface = pygame.Surface(rect.size)
        self.draw_network(newwork_surface)

        self.screen.blit(pygame.transform.flip(newwork_surface, not flipped, False), rect)


def interplate(a: float, b: float, t: float) -> float:
    return a + (b - a) * t