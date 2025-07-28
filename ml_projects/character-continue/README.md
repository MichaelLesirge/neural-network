# Character Prediction

<p>
The goal of this was to train a simple neural network to predict the next character in a string, using my own neural network library in this repo. On my first attempt after training it only returned the letter E, most likely due to it being the most common letter in the English language, but with a few more layers and different training data, it was able to form words in a way that was readable, and to my surprise even sometimes made some sense.

The pretrained networks in here (A, B, and C) were trained on these texts: The Bible, The Bee Movie script, The Shrek script, The Entire SouthPark script, and some other stuff I copy and pasted into the data file. These were mostly chosen based on how easy it was for me to find them and paste them into the document.
</p>

### GIF of interacting with trained network c using predict_next_char.py
 ![gif of using predict_next_char.py in console](https://github.com/user-attachments/assets/0d81e016-1437-4f90-8977-b2fdd4d0897c)

## Details of Training (predict_next_char_train.py)
The training program splits the document into the list of individual lines, with each line becoming a string. It then splits those strings into N (default N=1) training data points, with each data point having an answer which is a random character in the string, and the question being the last 25 characters leading up to it. Those question characters are then one hot encoded and trained in batches of 16, using CategoricalCrossEntropy as an error function to do back propagation with a high learning rate of ~0.01.


## Details of User Program (predict_next_char.py)
The program allows users to type in a string as input (like a prompt), and then feed that to the network to predict the next char and return that, repeating until a termination is reached (normally the network predicting a newline character). It chooses the next char by taking the N (default N=3) next to most likely chars according to the network, and randomly choosing one of them, with there likelihood according to the network serving as the weight in the random choice.

## Details of Network (network_util.py)
The network is a simple deep neural network (DNN). It has 3 hidden layers with 1024 neurons, using the [RELU](https://en.wikipedia.org/wiki/Rectifier_(neural_networks)) action function (RELU is just X if (X > 0)  else 0). The input layer takes in 25 characters, each as a one hot encoded vector of length 95 (one hot means there are 94 zeros and a single one, where the each location of a one represents a different character) for the 95 possible input characters, for a total input of 2375. The output layer returns the vector of a character, where each value represents the likelihood of that character. The output is then run though [SoftMax](https://en.wikipedia.org/wiki/Softmax_function) to get a normalized probability distribution.

```python
# Constants
MIN_CHAR = ord(" ")
MAX_CHAR = ord("~")
NUMBER_OF_CHARS_IN_RANGE = MAX_CHAR - MIN_CHAR + 1

MAX_CHARS_IN_DATA = 25

NETWORK_INPUT_LAYER_SIZE = NUMBER_OF_CHARS_IN_RANGE * MAX_CHARS_IN_DATA
NETWORK_HIDDEN_LAYER_SIZE = 2**10
NETWORK_OUTPUT_LAYER_SIZE = NUMBER_OF_CHARS_IN_RANGE

# Network
network = nn.network.Network([
    nn.layers.Dense(NETWORK_INPUT_LAYER_SIZE, NETWORK_HIDDEN_LAYER_SIZE),
    nn.activations.ReLU(),
    
    nn.layers.Dense(NETWORK_HIDDEN_LAYER_SIZE, NETWORK_HIDDEN_LAYER_SIZE),
    nn.activations.ReLU(),

    nn.layers.Dense(NETWORK_HIDDEN_LAYER_SIZE, NETWORK_HIDDEN_LAYER_SIZE),
    nn.activations.ReLU(),

    nn.layers.Dense(NETWORK_HIDDEN_LAYER_SIZE, NETWORK_HIDDEN_LAYER_SIZE),
    nn.activations.ReLU(),
    
    nn.layers.Dense(NETWORK_HIDDEN_LAYER_SIZE, NUMBER_OF_CHARS_IN_RANGE),
    nn.activations.Softmax(),    
], loss=nn.losses.CategoricalCrossEntropy())
```

## More Demos of Model
GIFs of trying out network B with predict_next_char. Mostly got gibberish but it is still kinda funny to see the results.
![Prompts With "I", Extra GIF of Network B](https://github.com/user-attachments/assets/f42a3b63-10f9-471b-b98a-e0af302b012b)
![More Random Prompts, Extra GIF of Network B](https://github.com/user-attachments/assets/f442066e-3133-4ba7-95f4-a2e4e525d07e)
![More Longer Prompts, Extra GIF of Network B](https://github.com/user-attachments/assets/96c6e834-903b-4f0d-9db6-d60163a16c02)












