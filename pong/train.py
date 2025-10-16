from main import BallConstants

from player import AIPaddle, BallPredictionPaddle

import numpy as np

MODEL = AIPaddle.SMALL_NETWORK
MODEL_FILE = AIPaddle.MODEL_SAVE_FILES[MODEL]

FUNCTION = BallPredictionPaddle.determine_direction

LOAD_PAST_MODEL = True

ROUNDS = 10000

TRAIN_N = 1_000_000
TEST_N = 1000

BATCH_SIZE = 2**6
EPOCHS = 20

LEARNING_RATE = 0.0005

def create_data(n: int):
    X_test = np.random.rand(n, AIPaddle.X_INPUT)

    # more realistic ball velocities
    directions = np.random.rand(n) * np.pi
    speeds = np.random.uniform(-BallConstants.MAX_VELOCITY, BallConstants.MAX_VELOCITY, size=(n,))
    X_test[:, 4] = np.cos(directions) * speeds
    X_test[:, 5] = np.sin(directions) * speeds

    # paddle normally on left or right side
    X_test[:, 0] = 1 - np.random.uniform(0, 1, size=(n,))

    y_test = np.array([FUNCTION(*x) for x in X_test])
    
    y_test = np.sign(y_test)

    y_test = y_test.reshape(-1, 1)

    return X_test, y_test

def main() -> None:
    print("Training AI Paddle model...")
    print(f"{ROUNDS=}, {TRAIN_N=}, {TEST_N=}")
    print(f"{BATCH_SIZE=}, {EPOCHS=}, {LEARNING_RATE=}")

    if LOAD_PAST_MODEL:
        MODEL.load(MODEL_FILE)
        print(f"Loaded past model from {MODEL_FILE}")

    X_test, y_test = create_data(TEST_N)

    print()
    predictions = MODEL.compute(X_test)
    initial_loss = MODEL.loss.forward(y_test, predictions)
    initial_accuracy = np.sum(np.sign(predictions) == np.sign(y_test))
    print(f"Test loss: {initial_loss}")
    print(f"Sign accuracy: {initial_accuracy} / {TEST_N} ({initial_accuracy / TEST_N:.2%})")

    for i in range(ROUNDS):
        print()
        print(f"Staring round {i + 1} of {ROUNDS} ({i / ROUNDS:.0%})")

        # Training data generation

        X_train, y_train = create_data(TRAIN_N)

        # Training

        print(f"Training on {X_train.shape} samples ({np.sum(y_train > 0)} positive, {np.sum(y_train < 0)} negative)")

        MODEL.train(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, learning_rate=LEARNING_RATE, logging=False)

        print()

        # Evaluation

        print("Evaluating model...")

        predictions = MODEL.compute(X_test)

        loss = MODEL.loss.forward(y_test, predictions)
        accuracy = np.sum(np.sign(predictions) == np.sign(y_test))

        print("Sample predictions:")
        for i in range(5):
            print(f"  Input: {X_test[i]}")
            print(f"  Prediction: {predictions[i][0]}, Actual: {y_test[i][0]}, Sign match: {(np.sign(predictions[i]) == np.sign(y_test[i]))[0]}, Loss: {MODEL.loss.forward(y_test[i], predictions[i])}")

        print(f"Test loss: {loss}")
        print(f"Sign accuracy: {accuracy} / {TEST_N} ({accuracy / TEST_N:.2%})")

        MODEL.dump(MODEL_FILE)
        print(f"Model saved to {MODEL_FILE}")

    print()
    print("Training complete. (100.00%)")

if __name__ == "__main__":
    main()