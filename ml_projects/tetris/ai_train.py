from datetime import datetime
from statistics import mean, median

import constants
import ai
from dqn_agent import DQNAgent
from tetris import Tetris

# Run dqn with Tetris
def dqn():
    
    env = Tetris(
        constants.BOARD_WIDTH, constants.BOARD_HEIGHT,
        enable_wall_kick=False, piece_queue_size=False, enable_hold=False
    )
    
    episodes = 2000
    epsilon_stop_episode = 1500
    mem_size = 20000
    discount = 0.95
    max_steps = float("inf")
    replay_start_size = 2000

    batch_size = 512
    epochs = 1
    
    train_every = 1

    render_every = 100
    log_every = 100

    agent = DQNAgent(ai.network,
                     epsilon_stop_episode=epsilon_stop_episode, mem_size=mem_size,
                     discount=discount, replay_start_size=replay_start_size)

    scores = []

    for episode in range(episodes):
        current_state = env.reset()
        done = False
        steps = 0 

        # Game
        while (not done) and (steps < max_steps):
            next_states: dict = env.get_next_states()
            best_state = agent.best_state(next_states.values())
            
            best_action = None
            for action, state in next_states.items():
                if state == best_state:
                    best_action = action
                    break

            state, reward, done, info = env.step(best_action)
            
            agent.add_to_memory(current_state, next_states[best_action], reward, done)
            current_state = next_states[best_action]
            steps += 1

        scores.append(info["score"])

        # Train
        if episode % train_every == 0:
            agent.train(batch_size=batch_size, epochs=epochs)

        # Render
        if render_every and episode % render_every == 0:
            print(env.render_as_str())

        # Logs
        if log_every and episode % log_every == 0:
            avg_score = mean(scores[-log_every:])
            min_score = min(scores[-log_every:])
            max_score = max(scores[-log_every:])

            print(f"{episode} {avg_score=}, {min_score=}, {max_score=}")


if __name__ == "__main__":
    dqn()