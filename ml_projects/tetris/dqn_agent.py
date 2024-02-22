from collections import deque
import numpy as np
import random

import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent.parent))

import neural_network as nn

class DQNAgent:
    def __init__(self, network: nn.network.Network, state_size: int, mem_size=10000, discount: float = 0.95,
                 epsilon: float = 1, epsilon_min: float = 0, epsilon_stop_episode: int = 500,
                 replay_start_size: int = None):

        # Out neural network
        self.network = network

        # Size of the input domain
        self.state_size = state_size
        
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
    
    def add_to_memory(self, current_state, next_state, reward, done) -> None:
        '''Adds a play to the replay memory buffer'''
        self.memory.append((current_state, next_state, reward, done))

    def random_value(self) -> float:
        '''Random score for a certain action'''
        return random.random()

    def predict_value(self, state) -> float:
        '''Predicts the score for a certain state'''
        return self.model.predict(state)[0]

    def act(self, state) -> float:
        '''Returns the expected score of a certain state'''
        state = np.reshape(state, [1, self.state_size])
        if random.random() <= self.epsilon:
            return self.random_value()
        else:
            return self.predict_value(state)

    def best_state(self, states):
        '''Returns the best state for a given collection of states'''
        max_value = None
        best_state = None

        if random.random() <= self.epsilon:
            return random.choice(list(states))

        else:
            for state in states:
                value = self.predict_value(
                    np.reshape(state, [1, self.state_size]))
                if not max_value or value > max_value:
                    max_value = value
                    best_state = state

        return best_state

    def train(self, batch_size = 32, epochs = 3) -> None:
        '''Trains the agent'''
        n = len(self.memory)

        if n >= self.replay_start_size and n >= batch_size:

            batch = random.sample(self.memory, batch_size)

            # Get the expected score for the next states, in batch (better performance)
            next_states = np.array([x[1] for x in batch])
            next_qs = [x[0] for x in self.model.predict(next_states)]

            x = []
            y = []

            # Build xy structure to fit the model in batch (better performance)
            for i, (state, _, reward, done) in enumerate(batch):
                if not done:
                    # Partial Q formula
                    new_q = reward + self.discount * next_qs[i]
                else:
                    new_q = reward

                x.append(state)
                y.append(new_q)

            # Fit the model to the given values
            self.model.fit(np.array(x), np.array(
                y), batch_size=batch_size, epochs=epochs, verbose=0)

            # Update the exploration variable
            if self.epsilon > self.epsilon_min:
                self.epsilon -= self.epsilon_decay
