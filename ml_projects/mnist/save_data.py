
# from keras.datasets.mnist import load_data
# import pickle

# (X_train, y_train), (X_test, y_test) = load_data()

# print(X_train.dtype, X_train.shape)
# print(y_train.dtype, y_train.shape)
# print(X_test.dtype, X_test.shape)
# print(y_test.dtype, y_test.shape)

# with open("ml_projects/mnist/mnist_train_test.pkl", "wb") as file:
#     data = ((X_train.shape[0], X_train.tobytes(), y_train.tobytes()), (X_test.shape[0], X_test.tobytes(), y_test.tobytes()))
#     print(len(data[0]), len(data[1]))
#     pickle.dump(data, file)