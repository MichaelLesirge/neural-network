import numpy as np
from matplotlib import pyplot as plt

# 10/10 book would recommend: https://nnfs.io/

def create_data(samples, classes):
    X = np.zeros((samples*classes, 2))
    y = np.zeros(samples*classes, dtype='uint8')
    for class_number in range(classes):
        ix = range(samples*class_number, samples*(class_number+1))
        r = np.linspace(0.0, 1, samples)
        t = np.linspace(class_number*4, (class_number+1)*4, samples) + np.random.randn(samples)*0.2
        X[ix] = np.c_[r*np.sin(t*2.5), r*np.cos(t*2.5)]
        y[ix] = class_number
    return X, y


X, y = create_data(samples=100, classes=3)

# plt.scatter(X[:,0], X[:,1], c = y, cmap="brg")
# plt.show()

class LayerDense:
    def __init__(self, n_inputs, n_outputs) -> None:
        # each row of weights aligns with one input, each column with one output
        self.weights = np.random.randn(n_inputs, n_outputs) * 0.01
        
        # each bias aligns with an output
        self.bias = np.zeros((1, n_outputs), dtype=float)

    def forward(self, inputs):
        """
        f(inputs, weights, biases) = inputs * weights + biases
        
        inputs = [[1, 2]]
        weights = [[3, 4, 5],
                   [6, 7, 8]]
        bias = [9, 10, 11]
        
        inputs       1,            2
                  /  |  \       /  |  \ 
        weights   3  4  5,      6  7  8    # imagine that both lines of a type went to the same neuron
        
        np.dot  1*3+2*6, 1*4+2*7, 1*5+2*8
                  3+12,    4+14,    5+16
                   15,      18,      21
                   
        bias       9,       10,      11
        
        np.add   15+9    10+18     21+11
        
        output     24      28        32
        """
        
        self.inputs = inputs
        self.output = np.dot(self.inputs, self.weights) + self.bias

    def backward(self, output_grad):
        """
        f(inputs, weights, biases) = inputs * weights + biases
        
        n(inputs) = f2(f(inputs, weights, biases), ...)

        n'(inputs) = f2'(f(inputs, weights, biases)) * f'(inputs, weights, biases)
        n'(inputs) = output_grad * f'(inputs, weights, biases)
        """
        
        """
        for weights
        f'(inputs, weights, biases) = inputs
        
        The width of `a` must be the same as the height `b`.
        'a' sets the height and 'b' sets the width
        
        batch_size = b = 1
        
        inputs = [[1, 2]]           shape = (b, 2), shape.T = (2, b)
        outputs_grad = [[3, 4, 5]]  shape = (b, 3)

        weights = [[3, 4, 5],       shape = (2, 3) <-- target
                   [6, 7, 8]]
                   
        solution: use inputs.T as first since it has correct height in wrong place, and its width will match the height of b.
        b has correct width so leave it as is, and the height will match the width of inputs.T
        """
        self.weights_grad = np.dot(self.inputs.T, output_grad)
        
        """
        for biases
        f'(inputs, weights, biases) = 1
        
        batch_size = b = 4
        output_grad = [[3, 4, 5],   shape = (b, 3)
                       [3, 4, 5],
                       [3, 4, 5],
                       [3, 4, 5]]
                       
        bias = [[9, 10, 11]]        shape = (1, 3)
        
        solution: sum down the columns, don't mean since with batches the goal is to do the work of many passes in one
        """
        self.bias_grad = np.sum(output_grad, axis=1, keepdims=True)

        """
        The width of `a` must be the same as the height `b`.
        'a' sets the height and 'b' sets the width
        
        for inputs
        f'(inputs, weights, biases) = weights
        
        batch_size = b = 1
        
        weights = [[3, 4, 5],       shape = (2, 3), shape.T = (3, 2)
                   [6, 7, 8]]
        outputs_grad = [[3, 4, 5]]  shape = (b, 3)

        inputs = [[1, 2]]           shape = (b, 2) <-- target
        """
        self.input_grad = np.dot(output_grad, self.weights.T)
        
class ActivationReLU:
    def forward(self, inputs):
        self.inputs = inputs
        """
        ReLU is 0 for all numbers bellow 0 and linear for numbers greater than zero
        """
        self.output = np.maximum(inputs, 0)
    
    def backward(self, output_grad):
        """
        0 is constant so it has a gradient of 0, if its greater than zero it is linear giving it a gradient of 1
        """
        output_grad = (self.inputs > 0).astype(float)
        self.inputs_grad = np.multiply(output_grad, output_grad)

class ActivationSoftmax:
    def forward(self, inputs):
        """
        softmax takes a row of values and converts into how likely that values is from 0 to 1, always with a sum of 1
        
        x = [[-1, 0.5, 1]]
        
        softmax(x) = [[0.07769558, 0.34820743, 0.57409699]]
        
        # 7.76%, 34.82%, 57.40%
        
        sum([[0.07769558, 0.34820743, 0.57409699]]) = 1.0
        

        the highest value of each row is subtracted to prevent exponential from overflowing, this has no effect on the final output though
        """
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        self.output = exp_values / np.sum(exp_values, axis=1, keepdims=True)
    
    def backward(self, output_grad):
        pass

class LossCategoricalCrossEntropy:
    def calculate(self, output_y, y):
        
        self.forward(output_y, y)
        
        return np.mean(self.output)

    def forward(self, y_pred, y_true):
        # clip value so that there can't be any zeros which would not work with log. Also clip on upper bound to keep it balanced
        y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
        
        if y_true.ndim == 1:
            """
            y_true is list of correct class

            y_pred = [[0.2, 0.7], [0.3, 0.6], [0.1, 0.9]]
            y_true = [1, 0, 1]
            correct_confidences = y_pred[[0, 1, 2], [1, 0, 1]] = [0.7, 0.3, 0.9]
            """
            correct_confidences = y_pred[range(np.size(y_true, axis=-1)), y_true]
        
        elif y_true.ndim == 2:
            """
            y_true is one hot encoded
            
            y_pred = [[0.2, 0.7], [0.3, 0.6], [0.1, 0.9]]
            y_true = [[0, 1], [1, 0], [0, 1]]
        
            y_pred * y_true = [[0, 0.7], [0.3, 0], [0, 0.9]]
            correct_confidences = np.sum([[0, 0.7], [0.3, 0], [0, 0.9]], axis=1) = [0.7, 0.3, 0.9]
            """
            correct_confidences = np.sum(y_pred * y_true, axis=1)
        """
        example of -log, rounded to 1 decimal
        
        -log(0.0) = inf
        -log(0.1) = 2.3
        -log(0.2) = 1.6
        -log(0.3) = 1.2
        -log(0.4) = 0.9
        -log(0.5) = 0.7
        -log(0.6) = 0.5
        -log(0.7) = 0.3
        -log(0.8) = 0.2
        -log(0.9) = 0.1
        -log(1.0) = 0.0
        """
        self.output = -np.log(correct_confidences)

    def backward(self, y_pred, y_true):
        n_samples = np.size(y_pred, 0)
        n_labels = np.size(y_pred, -1)
        
        if y_true.ndim == 1:
            # if y_true is list of labels, convert to one hot encoded
            y_true = np.eye(n_labels)[y_true]
            
        # -y_true = [[0, -1, 0], [0, -1, 0], [0, -1, 0]]
        #  y_pred = [[0.3, 0.4, 0.3], [0.2, 0.5, 0.3], [0.4, 0.2, 0.4]]
        # -y_true / y_pred = [[0, -2.5, 0], [0, -2, 0], [0, -5, 0]]
        self.inputs_grad = (-y_true / y_pred) / n_samples

dense1 = LayerDense(2, 3)
activation1 = ActivationReLU()

dense2 = LayerDense(3, 3)
activation2 = ActivationSoftmax()

loss_func = LossCategoricalCrossEntropy()

dense1.forward(X)
activation1.forward(dense1.output)

dense2.forward(activation1.output)
activation2.forward(dense2.output)

output = activation2.output

loss = loss_func.calculate(output, y)

predictions = np.argmax(output, axis=1)
if len(y.shape) == 2: class_targets = np.argmax(y, axis=1)
else: class_targets = y
accuracy = np.mean(predictions==class_targets)

print(f"loss = {loss}, accuracy = {accuracy:%}")

loss_func.backward(output, y)
print(loss_func.inputs_grad)