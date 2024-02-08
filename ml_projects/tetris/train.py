import pickle

import numpy as np

import ai

def load_training_data(name: str) -> tuple[np.ndarray, np.ndarray]:
    with open(name + "_x.pkl", "rb") as file:
        x = np.frombuffer(pickle.load(file), dtype=np.int8)
        x = x.reshape((x.size // ai.n_inputs, ai.n_inputs))
    with open(name + "_y.pkl", "rb") as file:
        y = np.frombuffer(pickle.load(file), dtype=np.int8)
    return (x, y)

def main() -> None:
    save_name = "a"
    training_x, training_y = load_training_data("ml_projects/tetris/" + save_name)
    
    nones: np.ndarray = training_y != ai.outputs.index(None)
    nones = np.logical_or(nones, np.random.random(nones.shape) < 1/8)
    
    print(training_y.shape)
    
    training_y = training_y[nones]
    training_x = training_x[nones]
    
    print(training_y.shape)
    
    values, counts = np.unique(training_y, return_counts=True)
    print(values[np.argmax(counts, axis=0)], dict(zip(values, counts)))
    
    # try:
    #     ai.network.load("ml_projects/tetris/tetris-network")
    # except FileNotFoundError:
    #     print("No starting file, starting run from scratch")
    # else:
    #     print("Training existing model")
        
    ai.network.train(training_x, training_y, batch_size=16, epochs=3, learning_rate=0.1)
    
    ai.network.dump("ml_projects/tetris/tetris-network")

if __name__ == "__main__":
    main()