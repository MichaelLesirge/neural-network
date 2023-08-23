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

    def forward(self, input):
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
        
        self.inputs = input
        self.outputs = np.dot(self.inputs, self.weights) + self.bias

    def backward(self, outputs_grad):
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
        self.weights_grad = np.dot(self.inputs.T, outputs_grad)
        
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
        self.bias_grad = np.sum(outputs_grad, axis=1, keepdims=True)

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
        self.inputs_grad = np.dot(outputs_grad, self.weights.T)
        
class ActivationReLU:
    def forward(self, inputs):
        self.inputs = inputs
        """
        ReLU is 0 for all numbers bellow 0 and linear for numbers greater than zero
        """
        self.outputs = np.maximum(inputs, 0)
    
    def backward(self, outputs_grad):
        """
        0 is constant so it has a gradient of 0, if its greater than zero it is linear giving it a gradient of 1
        """
        inputs_grad = (self.inputs > 0).astype(float)
        self.inputs_grad = np.multiply(inputs_grad, outputs_grad)

class ActivationSoftmax:
    def forward(self, inputs):
        """
        softmax takes a row of values and converts into how likely that values is from 0 to 1, always with a sum of 1
        
        x = [[-1, 0.5, 1]]
        
        softmax(x) = [[0.07769558, 0.34820743, 0.57409699]]
        
        7.76%, 34.82%, 57.40%
        
        sum([[0.07769558, 0.34820743, 0.57409699]]) = 1.0
        
        S(Z_i) = exp(Z_i) / sum(exp(Z))
        """
        
        # exp makes all values positive with the more negative a number is the closer to 0 it is
        # the highest value of each row is subtracted to prevent exponential from overflowing, this has no effect on the final output though
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        # since all values are now positive you can get what percent chance they are likely by
        self.outputs = exp_values / np.sum(exp_values, axis=1, keepdims=True)
    
    def backward(self, outputs_grad):      
        """
        thanks https://youtu.be/09c7bkxpv9I
        
        Z = [Z_1, Z_2, Z_3]

        --- Softmax ---
        S(Z_i) = exp(Z_i) / (exp(Z_1) + exp(Z_2) + exp(Z_3))
        S(Z_i) = exp(Z_i) / sum(exp(Z))

        --- Grad for Z_1 if i == j ---
        S(Z_1) = exp(Z_1) / (exp(Z_1) + exp(Z_2) + exp(Z_3))

        gradient rule for division:
        f(x) = g(x) / h(x)
        f'(x) = (g'(x) * h(x) - g(x) * h'(x)) / h(x)^2

        S(Z_1) = (exp(Z_1) * (exp(Z_1) + exp(Z_2) + exp(Z3)) - exp(Z_1) * (exp(Z_1) + exp(Z_2) + exp(Z_3))) / (exp(Z_1) + exp(Z_2) + exp(Z_3))^2

        other variables are treated as constants and the derivative of a added constant is 0
        S'(Z_1) = (exp(Z_1) * (exp(Z_1) + exp(Z_2) + exp(Z3)) - exp(Z_1) * (exp(Z_1) + 0 + 0)) / (exp(Z_1) + exp(Z_2) + exp(Z3))^2

        replace with sums for readability
        S'(Z_1) = (exp(Z_1) * sum(exp(Z)) - exp(Z_1) * exp(Z_1)) / sum(exp(Z))^2

        reorganize
        instead of x*y - x*x subtract the x x times before so it is x*(y-x)
        (10 * 7 - 10 * 2) = 50
        (10 * (7 - 2) = 50

        S'(Z_1) = exp(Z_1) * (sum(exp(Z)) - exp(Z_1)) / sum(exp(Z))^2

        split
        S'(Z_1) = exp(Z_1) * (sum(exp(Z)) - exp(Z_1)) / sum(exp(Z)) * sum(exp(Z))

        S'(Z_1) = (exp(Z_1) / sum(exp(Z))) * ((sum(exp(Z)) - exp(Z_1))) / sum(exp(Z))) 
        
        divide by denominator for second part  
        (10 - 3) / 4 = 1.75
        10 / 4 - 3 / 4 = 1.75
        
        (4 - 2) / 4 = 0.5
        1 - (2 / 4) = 0.5
        
        S'(Z_1) = (exp(Z_1) / sum(exp(Z))) * (1 - exp(Z_1) / sum(exp(Z)))
         
        replace
        S'(Z_1) = S(Z_1) * (1 - S(Z_1))
        
        --- Grad for Z_1 if i != j ---
        S(Z_2) = exp(Z_2) / (exp(Z_1) + exp(Z_2) + exp(Z_3))
        
        S'(Z_2) = (0 * sum(exp(Z)) - exp(Z_2) * (exp(Z_1) + 0 + 0)) / (exp(Z_1) + exp(Z_2) + exp(Z_3))**2
        
        get rid of zeros and replace with sum
        S'(Z_2) = (-exp(Z_2) * exp(Z_1)) / sum(exp(Z))**2
        
        split
        S'(Z_2) = (-exp(Z_2) * exp(Z_1)) / (sum(exp(Z)) * sum(exp(Z)))
        S'(Z_2) = (-exp(Z_2) / sum(exp(Z))) * (exp(Z_1) / sum(exp(Z)))
        
        replace with S
        
        --- Final ---
        
        for Z_1
        if i==j: S'(Z_1) = S(Z_1) * (1 - S(Z_1))
        else S'(Z_2) = -S(Z_2) * S(Z_1)
        
        combine
        S'(Z_i) = S(Z_1) * (int(i==j) - S(Z_j))
        """
     
        # create blank array for final grad
        self.inputs_grad = np.empty_like(outputs_grad)
        
        for index, (single_output, single_grad) in enumerate(zip(self.outputs, outputs_grad)):
            # output = [1, 2, 3, 4]
            # grad = [1, 1, 1, 1]
            
            # convert single_output to 2d
            single_output = single_output.reshape(1, -1)
            # output = [[1, 2, 3, 4]]
            
            """
            i is number softmax is being used on, j number we are getting the gradient of 
            
            S(Z_i) = exp(Z_i) / sum(exp(Z))
            S'(Z_j) = S(Z_i) * (int(i==j) - S(Z_j))
            
            reformat to:
            S'(Z_i) = (i if i==j else 0) - S(Z_i) * S(Z_j)
            
            --- i * j ---
            
            get S(Z_i) * S(Z_j)
            pick any i and j from output and there product is at those indices in this matrix
            np.dot(x.T, x)
            [[ 1,  2,  3,  4],
             [ 2,  4,  6,  8],
             [ 3,  6,  9, 12],
             [ 4,  8, 12, 16]]
             
            --- x - (i * j) ---
            
            get the (i == j) section. 
            Since here it is subtracted from first instead of it being subtracted from S(Z_j) the 
            4 * (1-2) = -4
            4 - (4 * 2) = -4
            
            4 * (0-2) = -8
            0 - (4 * 2) = -8
            
            np.diagflat(x)
            [[1, 0, 0, 0],
             [0, 2, 0, 0],
             [0, 0, 3, 0],
             [0, 0, 0, 4]]
             
            np.diagflat(x) - np.dot(x.T, x)
            [[  0,  -2,  -3,  -4],
             [ -2,  -2,  -6,  -8],
             [ -3,  -6,  -6, -12],
             [ -4,  -8, -12, -12]]
             
            #  --- final ---
            
            pick any i and j to test. pick to indexes from output
            
            derivative for i
            if i==j: S'(Z_i) = S(Z_i) * (1 - S(Z_j))
            if i!=j: S'(Z_j) = -S(Z_j) * S(Z_i)
              
            S'(Z_i)= S(Z_i) * (int(i==j) - S(Z_j))
            """
            
            jacobian_matrix = np.diagflat(single_output) - np.dot(single_output.T, single_output) 
            
            """
            multiply each column by corresponding grad value, then sum it across that row
            np.dot(np.diagflat(x) - np.dot(x.T, x), [1, 1, 1, 1])
            
            [ -9, -18, -27, -36]
            """
            self.inputs_grad[index] = np.dot(jacobian_matrix, single_grad)
            

class LossCategoricalCrossEntropy:
    def calculate(self, outputs_y, y):
        
        self.forward(outputs_y, y)
        
        return np.mean(self.outputs)

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
        self.outputs = -np.log(correct_confidences)

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



a = ActivationSoftmax()
l = LossCategoricalCrossEntropy()

input = np.array([[0.2, 1.8]])
true = np.array([[0, 1]])

print(input, true)

a.forward(input)
print(a.outputs)

l.forward(a.outputs, true)
print(l.outputs)

l.backward(a.outputs, true)
print(l.inputs_grad)

a.backward(l.inputs_grad)
print(a.inputs_grad)

# dense1 = LayerDense(2, 3)
# activation1 = ActivationReLU()

# dense2 = LayerDense(3, 3)
# activation2 = ActivationSoftmax()

# loss_func = LossCategoricalCrossEntropy()

# dense1.forward(X)
# activation1.forward(dense1.outputs)

# dense2.forward(activation1.outputs)
# activation2.forward(dense2.outputs)

# output = activation2.output

# loss = loss_func.calculate(output, y)

# predictions = np.argmax(output, axis=1)
# if len(y.shape) == 2: class_targets = np.argmax(y, axis=1)
# else: class_targets = y
# accuracy = np.mean(predictions==class_targets)

# print(f"loss = {loss}, accuracy = {accuracy:%}")

# loss_func.backward(output, y)
# print(loss_func.inputs_grad)