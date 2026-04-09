from main import BallConstants

from player import AIPaddle, BallPredictionPaddle

import numpy as np

MODEL = AIPaddle.DEFAULT_NETWORK
MODEL_FILE = AIPaddle.MODEL_SAVE_FILES[MODEL]

def function(*args):
    return BallPredictionPaddle.determine_direction(*args, handle_bounces=True)

def accuracy_function(y_true, y_pred):
    return np.sign(y_true) == np.sign(y_pred)

LOAD_PAST_MODEL = True

ROUNDS = 10000

TRAIN_N = 1_000_000
TEST_N = 1000

BATCH_SIZE = 2**6
EPOCHS = 20

def leanring_rate_schedule(iteration: int) -> float:
    if LOAD_PAST_MODEL:
        return 0.0005

    if iteration < 20:
        return 0.05
    elif iteration < 50:
        return 0.01
    elif iteration < 100:
        return 0.005
    else:
        return 0.0005

VISUIZE_DATA = False

def create_data(n: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns:
        np.ndarray: Test data with shape (n, 6), where each row is [paddle_x, paddle_y, ball_x, ball_y, ball_vel_x, ball_vel_y]
    """

    X_test = np.random.rand(n, AIPaddle.X_INPUT)

    # polar coordinates for ball velocity
    directions = np.random.uniform(0, 2 * np.pi, size=n)
    speeds = np.abs(np.random.normal(0, BallConstants.MAX_VELOCITY / 3, size=n))

    X_test[:, 4] = np.cos(directions) * speeds
    X_test[:, 5] = np.sin(directions) * speeds

    # paddle normally on left or right side
    a = 6
    b = 94
    paddles = np.where(np.random.rand(n) < 0.5, np.random.beta(a, b, size=(n,)), np.random.beta(b, a, size=(n,)))
    X_test[:, 0] = np.where(np.random.rand(n) < 0.3, paddles, X_test[:, 0])

    y_test = np.fromiter((function(*x) for x in X_test), dtype=float)
    y_test = np.sign(y_test)
    y_test = y_test.reshape(-1, 1)

    return X_test, y_test

def main() -> None:
    print("Training AI Paddle model...")
    print(f"{ROUNDS=}, {TRAIN_N=}, {TEST_N=}")
    print(f"{BATCH_SIZE=}, {EPOCHS=}")
    print()

    if LOAD_PAST_MODEL:
        MODEL.load(MODEL_FILE)
        print(f"Loaded past model from {MODEL_FILE}")

    X_test, y_test = create_data(TEST_N)

    if VISUIZE_DATA:
        plotted = 100
        from matplotlib import pyplot

        pyplot.plot(X_test[:plotted, 0], X_test[:plotted, 1], 'o', alpha=0.5)
        pyplot.xlabel("Paddle X Position")
        pyplot.ylabel("Paddle Y Position")
        pyplot.title("Paddle Positions in Test Data")
        pyplot.show()

        pyplot.quiver(X_test[:plotted, 2], X_test[:plotted, 3], X_test[:plotted, 4], X_test[:plotted, 5], angles='xy', scale_units='xy', scale=BallConstants.MAX_VELOCITY)
        pyplot.xlabel("Ball X Position")
        pyplot.ylabel("Ball Y Position")
        pyplot.title("Ball Positions and Velocities in Test Data")
        pyplot.show()

    print()
    predictions = MODEL.compute(X_test)
    initial_loss = MODEL.loss.forward(y_test, predictions)
    initial_accuracy = np.sum(accuracy_function(y_test, predictions))
    print(f"Test loss: {initial_loss}")
    print(f"Sign accuracy score: {initial_accuracy} / {TEST_N} ({initial_accuracy / TEST_N:.2%})")

    for i in range(ROUNDS):
        print()

        learning_rate = leanring_rate_schedule(i)

        print(f"Staring round {i + 1} of {ROUNDS} ({i / ROUNDS:.0%}), learning rate: {learning_rate})")

        # Training data generation

        X_train, y_train = create_data(TRAIN_N)

        # Training

        print(f"Training on {X_train.shape} samples ({np.sum(y_train > 0)} positive, {np.sum(y_train < 0)} negative)")

        MODEL.train(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, learning_rate=learning_rate, logging=False)

        print()

        # Evaluation

        print("Evaluating model...")

        predictions = MODEL.compute(X_test)

        loss = MODEL.loss.forward(y_test, predictions)
        accuracy = np.sum(accuracy_function(y_test, predictions))

        accuracy_change = accuracy - initial_accuracy

        print("Sample predictions:")
        for i in range(5):
            print(f"  Input: {X_test[i]}")
            print(f"  Prediction: {predictions[i][0]}, Actual: {y_test[i][0]}, Sign match: {(np.sign(predictions[i]) == np.sign(y_test[i]))[0]}, Loss: {MODEL.loss.forward(y_test[i], predictions[i])}")

        print(f"Test loss: {loss}")
        print(f"Sign accuracy score: {accuracy} / {TEST_N} ({accuracy / TEST_N:.2%})")
        print(f"Sign accuracy score change from initial: {accuracy_change:+}")

        MODEL.dump(MODEL_FILE)
        print(f"Model saved to {MODEL_FILE}")

    print()
    print("Training complete. (100.00%)")

if __name__ == "__main__":
    main()