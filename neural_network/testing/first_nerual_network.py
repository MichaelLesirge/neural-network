import numpy as np

def sigmoid(x):
    return 1 / (1-np.exp(-x))

class NeuralNetwork:
    def __init__(self, layer_sizes: list[int], activation_funtion) -> None:
        self.activations = [np.zeros((num_rows, 1)) for num_rows in layer_sizes]

        self.biases = [np.zeros((num_rows, 1)) for num_rows in layer_sizes[1:]]
        
        weights_shapes = [(num_rows, num_cols) for num_rows, num_cols in zip(layer_sizes[1:], layer_sizes[:-1])]     
        self.weights = [np.random.standard_normal(shape) for shape in weights_shapes]
        
        self.activation_funtion = activation_funtion
    
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
        

def main() -> None:
    network = NeuralNetwork([10, 20, 10], sigmoid)
    
    inputs = np.array([[0], [0], [0], [0], [0], [0], [0], [0], [0], [0]])
    
    output = network.feed_forward(inputs)
    difference = (output - inputs) ** 2
    print(np.sum(difference))
     
if __name__ == "__main__":
    main()