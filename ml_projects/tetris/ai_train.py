from statistics import mean

import numpy as np

import constants
import ai
from dqn_agent import DQNAgent
from tetris import Tetris

# Run dqn with Tetris
def main():
    
    env = Tetris(
        constants.BOARD_WIDTH, constants.BOARD_HEIGHT,
        enable_wall_kick=False, piece_queue_size=False, enable_hold=False
    )
    
    episodes = 20000
    epsilon_stop_episode = 15000
    mem_size = 20000
    discount = 0.95
    max_steps = float("inf")
    replay_start_size = 6000

    batch_size = 512
    epochs = 1
    learning_rate = 0.01
    
    train_every = 1

    render_every = 100
    log_every = 100

    agent = DQNAgent(ai.network, ai.state_size,
                     learning_rate=learning_rate,
                     epsilon_stop_episode=epsilon_stop_episode,
                     mem_size=mem_size,
                     discount=discount,
                     replay_start_size=replay_start_size)

    scores = []
    rewards = []
    
    move_counter = {move: 0 for move in ai.potential_moves}

    for episode in range(episodes):
        env.reset()
        
        current_state = env.game_to_inputs()
        
        done = False
        steps = 0 

        # Game
        while (not done) and (steps < max_steps):
            next_states = env.get_next_states(ai.potential_moves)
            
            best_state = agent.best_state(next_states.values())
            
            # reverse lookup on dict
            best_action = None
            for action, state in next_states.items():
                if np.array_equal(state, best_state):
                    best_action = action
                    break

            move_counter[best_action] += 1
            state, reward, done, info = env.step([best_action])
                        
            agent.add_to_memory(current_state, reward, done, next_states[best_action])
            
            current_state = next_states[best_action]
            
            steps += 1

        scores.append(info["score"])
        rewards.append(reward)

        # Train
        if episode % train_every == 0:
            agent.train(batch_size=batch_size, epochs=epochs)

        # Render
        if render_every and episode % render_every == 0:
            print(env.render_as_str())

        # Logs
        if episode % log_every == 0:
            print(f"Episode #{episode} ({episode / episodes:.1%})")

            avg_score = mean(scores[-log_every:])
            min_score = min(scores[-log_every:])
            max_score = max(scores[-log_every:])

            print(f"{avg_score = }, {min_score = }, {max_score = }")

            avg_reward = mean(rewards[-log_every:])
            min_reward = min(rewards[-log_every:])
            max_reward = max(rewards[-log_every:])

            print(f"{avg_reward = }, {min_reward = }, {max_reward = }")

            avg_score = mean(scores)
            avg_reward = mean(rewards)
            print(f"Overall: {avg_score = }, {avg_reward = }")
            
            print({move.name if move else "NONE": count for (move, count) in move_counter.items()})
            move_counter = {move: 0 for move in move_counter}
            
            print()
    
    print(f"Episode #{episode} (100%): {avg_score=}, {min_score=}, {max_score=}\n")
    
    ai.save()


if __name__ == "__main__":
    main()