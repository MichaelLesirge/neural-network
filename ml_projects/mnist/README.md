# MNIST
The MNIST database (Modified National Institute of Standards and Technology database) is a large collection of handwritten digits (zero to nine). It has a training set of 60,000 examples, and a test set of 10,000 examples. The images are monochrome and just 28 by 28 pixels.

## Network
The model uses my own feed forward neural network to predict it's answers. It takes the 28 by 28 grid as input with 784 neurons and outputs how likly each digit is from it's 10 output neurons. It has 3 hidden layers each with 256 neurons each. I use the RELU activation function for each deep layer and use softmax for the outputs. It was trained using the categorical cross entropy loss.

## Results
The model could correctly classify a digit 96.45% of the time on the test set. For reference the best model as of 2020 gets an accuracy of 99.87%. 

## Live Demo
This is a live demo of my model after being trained on the MNIST dataset. I made the drawing GUI with Tkinter, Python's built-in interface for Tcl/Tk. When you draw you are also drawing on a 28 by 28 grid that is then fed into the network giving a percentage chance of each digit. The digit with the highest percentage is then shown on the other side along with a silly message saying giving an idea of the confidence. You can press the buttons below the drawing board to see the image in the form of a Matplotlib graph to get an idea of what the model sees.

<img alt="python MNIST drawing GUI" src="https://github.com/michael-lesirge/neural-network/assets/100492377/27856ede-a556-4ee0-bbe1-7aba370cb57e">
