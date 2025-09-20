# Neural Network from scratch in Python

<img align="right" alt="Neural network code" src="https://github.com/michael-lesirge/neural-network/assets/100492377/24a82054-6954-4676-8360-aabab90802f4" width = 500>
<p>
Very basic neural network module that I made in Python using NumPy. It allows you to create neural networks and train them with a simple API, inspired by TensorFlow's Keras.

I tried to keep a clean and extendable project structure, allowing for new additions of layers to be added easily. I have currently implemented dense layers, multiple activation functions, multiple loss functions, and a network class to bring them all together.

This project was mostly made with the goal of getting a basic understanding how neural networks and deep learning works, and just to say I did it from scratch.

</p>

<br clear="right"/>

## Progress

Currently Implemented:
- Fully Connect / Dense Layer (a layer in a neural network that connects each neuron in a layer to every neuron in the previous layer)
- Many common activation functions (Sigmoid, Tanh, ReLU, Softmax, etc)
- Common loss functions (MSE, Categorical Cross Entropy, Binary Cross Entropy)
- A network class that allows for easy usages of implemented layers, and allows for easy training with back propagation and easy usage with forward propagation.
- Storing network by saving and loading it from file
  
TODO:
- Convolutional, maxpool, and dropout layers for convolutional neural networks (CNNs)

## Handwritten Digit Classifier [ml_projects/mnist](https://github.com/MichaelLesirge/neural-network/tree/main/ml_projects/mnist)
<p>This is a demo of a model trained to classify handwritten digits from the MNIST dataset. It correctly labels 96.45% of the test data, which I am pretty happy with. I made the drawing GUI with Tkinter and all additional plots/graphs with Matplotlib. This was the first real data I attempted to train my network with.</p>
<img alt="mnist drawing gui GIF" src="https://github.com/michael-lesirge/neural-network/assets/100492377/27856ede-a556-4ee0-bbe1-7aba370cb57e">

## Tetris (In Progress) [ml_projects/tetris](https://github.com/MichaelLesirge/neural-network/tree/main/ml_projects/tetris)
<p>This was my first time attempting anything with reinforcement learning. I created a DQN agent to try and play tetris. I liked the Tetris clone I made, but my AI for the game was subpar (a handwritten AI would do much better). I want to come back to this though (tetris2) and do it better. Currenly it has no incentive to play quickly and it learned harddrop may cause it to lose faster, so gameplay is a bit slow.</p>
<img alt="AI playing tetris" src="https://github.com/user-attachments/assets/709f2d4e-c8f9-4eb4-bb8a-06664031d181">

## Character Predictions [ml_projects/character-continue](https://github.com/MichaelLesirge/neural-network/tree/main/ml_projects/character-continue)
<p>This is a demo of the model trained to predict the next character. It was based on a variety of text files I found on the internet, including the Shrek and Bee Movie script, the entirety of the Bible and Harry Potter, all Shakespeare's works, and some other random stuff I found. To interact (as shown in the demo) you start typing out some characters, and it keeps on guessing what will come next until it guesses a new line character (\n) which terminates the message. I am pretty happy it even generates words but it is definitely overfit on the data.</p>
<img alt="using predict_next_char.py in console GIF" src="https://github.com/user-attachments/assets/0d81e016-1437-4f90-8977-b2fdd4d0897c">

## Installation & Setup

1. Clone the repository
   ```bash
   git clone https://github.com/MichaelLesirge/neural-network.git
   cd neural-network
   ```

2. Create a virtual environment

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment
   
   On Windows: ```.venv\Scripts\activate```
   
   On macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```

5. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
