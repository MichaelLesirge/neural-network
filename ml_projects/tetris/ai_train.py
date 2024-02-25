import numpy as np

import constants
from dqn_agent import DQNAgent
from tetris import Tetris

# Run dqn with Tetris
def main():
    
    env = Tetris(
        constants.BOARD_WIDTH, constants.BOARD_HEIGHT,
        enable_wall_kick=True, piece_queue_size=False, enable_hold=False
    )
    
    episodes = 200_000
    epsilon_stop_episode = episodes * 0.9

    max_steps = float("inf")

    batch_size = 512
    epochs = 1
    
    train_every = 1

    render_every = 100
    log_every = 100

    # ai.load()
    
    agent = DQNAgent(constants.NETWORK, constants.STATE_SIZE,
                     learning_rate=0.01,
                     epsilon_stop_episode=epsilon_stop_episode,
                     mem_size=10_000,
                     discount=0.95,
                     replay_start_size=6000)

    scores = []
    average_game_rewards = []
    
    move_counter = {move: 0 for move in constants.POTENTIAL_MOVES}

    for episode in range(episodes):
        env.reset()
                
        done = False
        steps = 0 
        
        game_rewards = []
        # Game
        while (not done) and (steps < max_steps):
            next_states = env.get_next_states(constants.POTENTIAL_MOVES)
            
            best_action = agent.best_action(next_states)

            move_counter[best_action] += 1
            state, reward, done, info = env.step([best_action])
                        
            agent.add_to_memory(state, reward, done, next_states[best_action])
                        
            game_rewards.append(reward)
            steps += 1

        average_game_rewards.append(np.mean(game_rewards))
        scores.append(info["score"])

        # Train
        if episode % train_every == 0:
            agent.train(batch_size=batch_size, epochs=epochs)

        # Render
        if render_every and episode % render_every == 0:
            print("END OF GAME:", info)
            print(env.render_as_str())
            y_true, y_pred = env.value_function(), agent.predict_value(env.state())
            print(f"{y_true=} {y_pred=}")

        # Logs
        if episode % log_every == 0:
            print(f"Episode #{episode} ({episode / episodes:.1%}). {agent.epsilon = }. ({constants.VERSION})")

            avg_score = np.mean(scores[-log_every:])
            min_score = min(scores[-log_every:])
            max_score = max(scores[-log_every:])

            print(f"{avg_score = }, {min_score = }, {max_score = }")

            avg_reward = np.mean(average_game_rewards[-log_every:])
            min_reward = min(average_game_rewards[-log_every:])
            max_reward = max(average_game_rewards[-log_every:])

            print(f"{avg_reward = }, {min_reward = }, {max_reward = }")

            avg_score = np.mean(scores)
            avg_reward = np.mean(average_game_rewards)
            print(f"Overall: {avg_score = }, {avg_reward = }")
            
            print({move.name if move else "NONE": count for (move, count) in move_counter.items()})
            move_counter = {move: 0 for move in move_counter}
            
            print()
            
    avg_score = np.mean(scores)
    avg_reward = np.mean(average_game_rewards)    
    print(f"Final Overall: {avg_score = }, {avg_reward = }")
    
    constants.NETWORK.dump(constants.SAVE_FILE_NAME)


if __name__ == "__main__":
    main()