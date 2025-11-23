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

# Projects
Here are a few projects I have created that make use of the neural network. I think they demonstrate the flexibility of even a simple neural network architecture to do a variety of tasks like: 
- classify (the network is trained to predict label of an item)
- playing (trained to predict which next more would minimize chance of losing)
- generating (predict what item would come next to extend the sequence with new content)

## Handwritten Digit Classifier [mnist](https://github.com/MichaelLesirge/neural-network/tree/main/mnist)
<p>This is a demo of a model trained to classify handwritten digits from the MNIST dataset. It correctly labels 96.45% of the test data, which I am pretty happy with. I made the drawing GUI with Tkinter and all additional plots/graphs with Matplotlib. This was the first real data I attempted to train my network with.</p>
<img alt="MNIST drawing GUI GIF" src="https://github.com/michael-lesirge/neural-network/assets/100492377/27856ede-a556-4ee0-bbe1-7aba370cb57e">

## Tetris [tetris](https://github.com/MichaelLesirge/neural-network/tree/main/tetris)
<p>This was my first time attempting anything with reinforcement learning. I created a DQN agent to try and play Tetris. I liked the Tetris clone I made, and decided to try and add an AI. I want to come back to this though (tetris2) and do it better. Currently it has no incentive to play quickly and it learned hard drop may cause it to lose faster, so gameplay is a bit slow, but it still gets there in the end.</p>
<img alt="AI playing Tetris" src="https://github.com/user-attachments/assets/709f2d4e-c8f9-4eb4-bb8a-06664031d181">

## Character Predictions [character-continue](https://github.com/MichaelLesirge/neural-network/tree/main/character-continue)
<p>This is a demo of the model trained to predict the next character. It was based on a variety of text files I found on the internet, including the Shrek and Bee Movie script, the entirety of the Bible and Harry Potter, all Shakespeare's works, and some other random stuff I found. To interact (as shown in the demo) you start typing out some characters, and it keeps on guessing what will come next until it guesses a new line character (\n) which terminates the message. I am pretty happy it even generates words but it is definitely overfit on the data.</p>
<img alt="using predict_next_char.py in console GIF" src="https://github.com/user-attachments/assets/0d81e016-1437-4f90-8977-b2fdd4d0897c">

## Pong [pong](https://github.com/MichaelLesirge/neural-network/tree/main/pong)
<p>This is a demo two competing models playing pong. The models get 6 inputs (paddle x, paddle y, ball x, ball y, ball vx, ball vy) and output either a positive or negative value which determines if the paddle moves up or down. You can pick player types in the start menu. In the neural network overlay, positive is blue and negative is red.</p>
<img alt="Pong AI vs AI game with overlay" src="https://github.com/user-attachments/assets/e5c9a635-00f8-41f9-acd7-86171f7c09b8">

## Experiments [random-practice](https://github.com/MichaelLesirge/neural-network/tree/main/random_practice)
All the things I made to get a better understanding of how neural networks work when I was early in writing my own version. They all have plenty of comments that I made when I was trying to wrap my head around it.
<img width="1000" alt="image" src="https://github.com/MichaelLesirge/neural-network/blob/main/random_practice/one_neuron_back_prop.gif" />


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

6. Run the main file of the project
   ```bash
   cd mnist
   python main.py
   ```
