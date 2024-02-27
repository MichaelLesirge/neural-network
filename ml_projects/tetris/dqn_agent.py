from collections import deque
import numpy as np
import random

import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent.parent))

import neural_network as nn

class DQNAgent:
    def __init__(self, name: str, state_size: int, learning_rate: float = 0.01, mem_size=10000, discount: float = 0.95,
                 epsilon: float = 1, epsilon_min: float = 0, epsilon_stop_episode: int = 500,
                 replay_start_size: int = None):

        self.name = name

        # The size of our state (model input size)
        self.state_size = state_size

        # Our model
        layer_size = 2 ** 8  # 256
        self.network = nn.network.Network([
            nn.layers.Dense(state_size, layer_size),
            nn.activations.ReLU(),

            nn.layers.Dense(layer_size, layer_size),
            nn.activations.ReLU(),
            
            nn.layers.Dense(layer_size, layer_size),
            nn.activations.ReLU(),
            
            nn.layers.Dense(layer_size, 1),
            nn.activations.Linear(),

        ], loss=nn.losses.MSE())
         
        # Learning rate for training
        self.learning_rate = learning_rate
        
        # Replay Buffer
        self.memory = deque(maxlen=mem_size)
        
        # Exploration (probability of random values given) value at the start
        self.epsilon = epsilon

        # How important is the future rewards compared to the immediate ones [0,1]
        self.discount = discount
        
        # At what epsilon value the agent stops decrementing it
        self.epsilon_min = epsilon_min
        
        # How much is subtracted for the epsilon after the min is hit
        self.epsilon_decay = (self.epsilon - self.epsilon_min) / (epsilon_stop_episode)
        
        # Minimum memory size needed to train
        if replay_start_size is None: replay_start_size = mem_size // 2
        self.replay_start_size = replay_start_size
        
        # Location to dump/load model to/from
        self.save_file = str(directory / self.name) + ".pkl"
    
    def add_to_memory(self, current_state: np.ndarray, reward: float, done: bool, next_state: np.ndarray) -> None:
        """Adds a play to the replay memory buffer"""
        self.memory.append((current_state, reward, done, next_state))

    def random_value(self) -> float:
        """Random score for a certain action"""
        return random.random()

    def predict_value(self, state: np.ndarray) -> float:
        """Predicts the score for a certain state"""
        return self.network.compute(state)[0]

    def best_state(self, states: list[np.ndarray]) -> np.ndarray:
        """Returns the best state for a given collection of state"""
        if (len(states) == 0): return None
         
        return max(states, key=self.predict_value)

    def take_action(self, next_states: dict[object, np.ndarray]) -> object:
        """Returns the best state for a given collection of state"""

        if random.random() <= self.epsilon: return random.choice(list(next_states.keys()))

        best_state = self.best_state(next_states)
 
        for action, state in next_states.items():
            if np.array_equal(state, best_state):
                return action

    def train(self, batch_size = 512, epochs = 1) -> None:
        """Trains the agent"""

        if len(self.memory) >= self.replay_start_size and len(self.memory) >= batch_size:

            batch = random.sample(self.memory, batch_size)

            # Get the expected score for the next states, in batch (better performance)
            next_states = np.array([next_state for (state, reward, done, next_state) in batch])
            next_qs = [y[0] for y in self.network.compute(next_states)]

            x = np.empty((len(batch), self.state_size), dtype=np.float64)
            y = np.empty((len(batch), 1), dtype=np.float64)

            # Build xy structure to fit the model in batch (better performance)
            for i, (state, reward, done, next_state) in enumerate(batch):
                if not done:
                    # Partial Q formula
                    new_q = reward + self.discount * next_qs[i]
                else:
                    new_q = reward

                x[i] = (state)
                y[i, 0] = (new_q)
                
            # Fit the model to the given values
            self.network.train(x, y, batch_size=batch_size, epochs=epochs, learning_rate=self.learning_rate, logging=False)

            # Update the exploration variable
            self.epsilon = max(self.epsilon_min, self.epsilon - self.epsilon_decay)

    def dump(self):
        self.network.dump(self.save_file)

    def dump(self):
        self.network.load(self.save_file)
        