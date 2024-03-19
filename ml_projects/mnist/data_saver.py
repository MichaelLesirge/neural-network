import pickle

small_drawing_width, small_drawing_height = (28, 28)

def save(directory):
    from keras.datasets.mnist import load_data

    (X_train, y_train), (X_test, y_test) = load_data()

    print(X_train.dtype, X_train.shape)
    print(y_train.dtype, y_train.shape)
    print(X_test.dtype, X_test.shape)
    print(y_test.dtype, y_test.shape)

    with open(directory / "mnist_train_test.pkl", "wb") as file:
        data = ((X_train.shape[0], X_train.tobytes(), y_train.tobytes()), (X_test.shape[0], X_test.tobytes(), y_test.tobytes()))
        print(len(data[0]), len(data[1]))
        pickle.dump(data, file)
        
def load(directory):
    import numpy as np
    
    with open(directory / "mnist_train_test.pkl", "rb") as file:
        ((train_len, X_train, y_train), (test_len, X_test, y_test)) = pickle.load(file)
        
        X_train = np.frombuffer(X_train, dtype=np.uint8).reshape((train_len, small_drawing_height, small_drawing_width))
        y_train = np.frombuffer(y_train, dtype=np.uint8).reshape((train_len,))
        
        X_test = np.frombuffer(X_test, dtype=np.uint8).reshape((test_len, small_drawing_height, small_drawing_width))
        y_test = np.frombuffer(y_test, dtype=np.uint8).reshape((test_len,))
        
        return (X_train, y_train), (X_test, y_test)