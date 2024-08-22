# Various projects using my Neural Network

The following are in order of how good I think they were as projects

## MNIST [ml_projects/mnist](https://github.com/MichaelLesirge/neural-network/tree/main/ml_projects/mnist)
<p>This is a demo of a model trained to classify handwritten digits from the MNIST dataset. It correctly labels 96.45% of the test data, which I am pretty happy with. I made the drawing GUI with Tkinter and all additional plots/graphs with Matplotlib. This was the first real data I attempted to train my network with.</p>
<img alt="python mnist drawing gui GIF" src="https://github.com/michael-lesirge/neural-network/assets/100492377/27856ede-a556-4ee0-bbe1-7aba370cb57e">

## Character Predictions [ml_projects/charter-continue](https://github.com/MichaelLesirge/neural-network/tree/main/ml_projects/charter-continue)
<p>This is a demo of the model trained to predict the next character. It was based on a variety of text files I found on the internet, including the Shrek and Bee Movie script, the entirety of the Bible and Harry Potter, all Shakespeare's works, and some other random stuff I found. To interact (as shown in the demo) you start typing out some characters, and it keeps on guessing what will come next until it guesses a new line character (\n) which terminates the message. I am pretty happy it even generates words but it is definitely overfit on the data.</p>
<img alt="using predict_next_char.py in console GIF" src="https://github.com/user-attachments/assets/c5f4ac51-284a-4c2a-b576-8992a8bbb47b">

## Tetris (In Progress) [ml_projects/tetris](https://github.com/MichaelLesirge/neural-network/tree/main/ml_projects/tetris)
<p>This was my first time attempting anything with reinforcement learning. I created a DQN agent to try and play tetris. I liked the Tetris clone I made, but my AI for the game was subpar (a handwritten AI would do much better). I want to come back to this though (tetris2) and do it better.</p>
<img alt="AI playing tetris" src="https://github.com/user-attachments/assets/709f2d4e-c8f9-4eb4-bb8a-06664031d181">

## Pong Game [ml_projects/pong_game](https://github.com/MichaelLesirge/neural-network/tree/main/ml_projects/pong_game)
<p>This was my first project I wanted to make an AI for. I made this simple pong game before I made a neural network or had any idea what I was doing. In the end I did not bother using a neural network for it, as a handwritten AI was better for such a simple problem. This GIF shows a player (left) against the simple AI (right)</p>
<img alt="pong game with human (left) vs ai (right)" src="https://github.com/michael-lesirge/neural-network/assets/100492377/55d8f5a6-caff-49b8-890f-b61c84cfda87">
