from pygame.math import Vector2 as Vec2

from main import PaddleConstants, BallConstants

from player import AIPaddle, BallPredictionPaddle

import numpy as np

MODEL = AIPaddle.MODEL

X_FUNCTION = lambda: np.array([
    np.random.choice([PaddleConstants.START_LOCATION.x, PaddleConstants.START_LOCATION.mirrored().x]),  # paddle_x
    np.random.rand(),  # paddle_y
    np.random.rand(),  # ball_x
    np.random.rand(),  # ball_y
    *Vec2.from_polar((np.random.rand() * BallConstants.MAX_VELOCITY, np.random.rand() * 360)).xy
])

# Y_FUNCTION = BallPredictionPaddle.determine_direction
Y_FUNCTION = lambda *args: np.sign(BallPredictionPaddle.determine_direction(*args))

LOAD_PAST_MODEL = True

ROUNDS = 10

TRAIN_N = 1_000_000
TEST_N = 1000

BATCH_SIZE = 2**6
EPOCHS = 20

LEARNING_RATE = 0.0005

BALANCE_TRAINING_SIGNS = True

def main() -> None:

    print("Training AI Paddle model...")
    print(f"{ROUNDS=}, {TRAIN_N=}, {TEST_N=}")
    print(f"{BATCH_SIZE=}, {EPOCHS=}, {LEARNING_RATE=}")

    if LOAD_PAST_MODEL:
        MODEL.load(str(AIPaddle.NETWORK_FILE))
        print(f"Loaded past model from {AIPaddle.NETWORK_FILE}")

    X_test = np.random.rand(TEST_N, AIPaddle.X_INPUT)
    y_test = np.array([Y_FUNCTION(*x) for x in X_test]).reshape(-1, 1)

    for i in range(ROUNDS):
        print()
        print(f"Staring round {i + 1} of {ROUNDS} ({i / ROUNDS:.0%})")

        # Training data generation

        X_train = np.array([X_FUNCTION() for _ in range(TRAIN_N)])

        y_train = np.array([Y_FUNCTION(*x) for x in X_train]).reshape(-1, 1)

        pos_indices = np.where(y_train > 0)[0]
        neg_indices = np.where(y_train < 0)[0]
        diff = len(pos_indices) - len(neg_indices)
        if diff != 0 and BALANCE_TRAINING_SIGNS:
            drop_indices = np.random.choice(pos_indices if diff > 0 else neg_indices, abs(diff), replace=False)
            X_train = np.delete(X_train, drop_indices, axis=0)
            y_train = np.delete(y_train, drop_indices, axis=0)

        # Training

        print(f"Training on {X_train.shape} samples ({np.sum(y_train > 0)} positive, {np.sum(y_train < 0)} negative)")

        MODEL.train(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, learning_rate=LEARNING_RATE, logging=True)

        print()

        # Evaluation

        print("Evaluating model...")

        predictions = MODEL.compute(X_test)

        loss = MODEL.loss.forward(y_test, predictions)
        sign_matches = np.sum(np.sign(predictions) == np.sign(y_test))

        print(f"Test MSE: {loss}")
        print(f"Sign accuracy: {sign_matches} / {TEST_N} ({sign_matches / TEST_N:.2%})")

        print("Sample predictions:")
        for i in range(10):
            print(f"  Input: {X_test[i]}")
            print(f"  Prediction: {predictions[i][0]}, Actual: {y_test[i][0]}, Sign match: {(np.sign(predictions[i]) == np.sign(y_test[i]))[0]}, Loss: {MODEL.loss.forward(y_test[i], predictions[i])}")

        MODEL.dump(str(AIPaddle.NETWORK_FILE))
        print(f"Model saved to {AIPaddle.NETWORK_FILE}")

    print()
    print("Training complete. (100.00%)")

if __name__ == "__main__":
    main()