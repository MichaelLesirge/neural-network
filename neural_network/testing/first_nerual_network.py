import numpy as np
from random import randint

def sigmoid(x):
    return 1 / (1-np.exp(-x))

class NeuralNetwork:
    def __init__(self, layer_sizes: list[int], activation_funtion = sigmoid) -> None:
        self.activations = [np.zeros((num_rows, 1)) for num_rows in layer_sizes]

        self.biases = [np.zeros((num_rows, 1)) for num_rows in layer_sizes[1:]]
        
        weights_shapes = [(num_rows, num_cols) for num_rows, num_cols in zip(layer_sizes[1:], layer_sizes[:-1])]     
        self.weights = [np.random.standard_normal(shape) for shape in weights_shapes]
        
        self.activation_funtion = np.vectorize(activation_funtion)
    
    def randomly_change_weight(self):
        pass
    
    def feed_forward(self, inputs):
        self.activations[0] = inputs
        
        for l in range(len(self.activations)-1):
            z = np.matmul(self.weights[l], self.activations[l]) + self.biases[l]
            self.activations[l+1] = self.activation_funtion(z)
        
        return self.activations[-1]
    
    def output_activation(self) -> None:
        print("\nActivations:")
        for a in self.activations: print(a, "\n")
            
    def output_biases(self) -> None:
        print("\nBiases:")
        for b in self.biases: print(b, "\n")
            
    def output_weights(self) -> None:
        print("\nWeights:")
        for w in self.weights: print(w, "\n")
        
def error(output: np.ndarray, correct: np.ndarray) -> float:
    return ((output - correct) ** 2).mean()

def make_input(n: int, *, size: int = 10):
    inputs = np.zeros((10, 1))
    inputs[n % size] = 1
    return inputs

def main() -> None:
    
    good_enough_error = 0.000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
    print(good_enough_error)
    best_network = None
    min_error = float("inf")
    
    while min_error > good_enough_error:
        network = NeuralNetwork([10, 20, 10], sigmoid)
    
        inputs = make_input(1) 
    
        outputs = network.feed_forward(inputs)
    
        cur_error = error(outputs, inputs)
        
        if cur_error < min_error:
            min_error = cur_error
            best_network = network
            print("Best min error:", min_error)
            print(outputs)
            print()
            print()
    
    print()
    
    while True:
        inputs = make_input(int(input("Number: "))) 
    
        outputs = best_network.feed_forward(inputs)
        
        print("activations:")
        print(outputs)

        cur_error = error(outputs, inputs)
        
        print("Error: ", cur_error)
        print("Guess: ", np.argmax(outputs))
        
        print()
     
if __name__ == "__main__":
    main()