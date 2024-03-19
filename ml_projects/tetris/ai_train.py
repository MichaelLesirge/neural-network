import time
import datetime

import numpy as np

import constants
from dqn_agent import DQNAgent
from tetris import Tetris

# Run dqn with Tetris
def main():

    fps = 1
    
    env = Tetris(
        constants.BOARD_WIDTH, constants.BOARD_HEIGHT, shape_queue_size=constants.SHAPE_QUEUE_SIZE,
        FPS=fps, enable_wall_kick=True, enable_hold=True,
    )
    
    episodes = 100_000
    epsilon_stop_episode = episodes * (75 / 100)
    epsilon_start = (100 / 100)

    max_steps = float("inf")

    batch_size = 512
    epochs = 1
    
    train_every = fps

    log_every = 100

    
    agent = DQNAgent(constants.AGENT_NAME, env.state_as_array().size,
                     learning_rate=0.01,
                     epsilon_stop_episode=epsilon_stop_episode,
                     mem_size=10_000,
                     discount=0.95,
                     replay_start_size=6000,
                     epsilon=epsilon_start)
    
    try:
        agent.load()
    except FileNotFoundError:
        print("No agent to load: Starting run from scratch")

    scores = []
    lines = []
    average_game_rewards = []
    log_delay_times = []
    log_start_time = time.time()
    
    try:
        for episode in range(episodes):
            env.reset()
                    
            done = False
            steps = 0 
            
            game_rewards = []
            
            # Game
            while (not done) and (steps < max_steps):
                next_states = env.get_next_states()
                
                best_action = agent.take_action(next_states)

                state, reward, done, info = env.step(best_action)
                
                # if not np.array_equal(next_states[best_action], state):
                #     print(env.render_as_str())
                #     print(abs(next_states[best_action].sum() - state.sum()))
                #     print(np.array2string((next_states[best_action] == state), max_line_width=6*10+2, separator=" "))
                #     raise Exception("State Match Failed")
                            
                agent.add_to_memory(state, reward, done, next_states[best_action])
                            
                game_rewards.append(reward)
                steps += 1

            average_game_rewards.append(np.mean(game_rewards))
            scores.append(info["score"])
            lines.append(info["lines"])

            # Train
            if episode % train_every == 0:
                agent.train(batch_size=batch_size, epochs=epochs)

            if episode % log_every == 0:
                log_delay_times.append(time.time() - log_start_time)
                log_start_time = time.time()
                
                print("END OF GAME:", info)
                print(env.render_as_str())
                y_true, y_pred = env.value_function(), agent.predict_value(env.state_as_array())[0]
                print(f"{y_true=}, {y_pred=}")
            
                expected_round_time = np.mean(log_delay_times[-10:])
                rounds_left = (episodes - episode) / log_every
                
                print(f"Episode #{episode}, ({episode / episodes:.1%}). {agent.epsilon=} ({agent.name})")
                print(f"Estimated Time: Total={datetime.timedelta(seconds=int(expected_round_time * rounds_left))}, Round={datetime.timedelta(seconds=expected_round_time)}")

                avg_score = np.mean(scores[-log_every:])
                min_score = min(scores[-log_every:])
                max_score = max(scores[-log_every:])

                print(f"{avg_score = }, {min_score = }, {max_score = }")

                avg_lines = np.mean(lines[-log_every:])
                min_lines = min(lines[-log_every:])
                max_lines = max(lines[-log_every:])

                print(f"{avg_lines = }, {min_lines = }, {max_lines = }")

                avg_reward = np.mean(average_game_rewards[-log_every:])
                min_reward = min(average_game_rewards[-log_every:])
                max_reward = max(average_game_rewards[-log_every:])

                print(f"{avg_reward = }, {min_reward = }, {max_reward = }")

                avg_score = np.mean(scores)
                avg_lines = np.mean(lines)
                avg_reward = np.mean(average_game_rewards)
                print(f"Overall: {avg_score = }, {avg_lines = }, {avg_reward = }")
                
                print()
                
        avg_score = np.mean(scores)
        avg_reward = np.mean(average_game_rewards)    
        print(f"Final Overall: {avg_score = }, {avg_reward = }")
    except KeyboardInterrupt:
        print("Stopping...")
        
    agent.dump() 


if __name__ == "__main__":
    main()