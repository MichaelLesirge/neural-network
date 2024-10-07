import tkinter as tk
import numpy as np
from network_util import *

# Parameters for prediction behavior
CHOOSE_N_CANDIDATES_FROM_TOP = 1
NETWORK_PATH = directory / "char-network-b"

# Load the network model
network.load(str(NETWORK_PATH))

def predict_next_character_probs(message, n = 7):
    output = network.compute(format_one_hot_messages(message_to_one_hot(message)))[0]
    top_indices = np.argsort(output)[:-n-1:-1]
    top_probabilities = output[top_indices]
    normalized_probabilities = top_probabilities / top_probabilities.sum()
    return top_indices, normalized_probabilities

def predict_next_word(message, max_len = 28):

    word = ""

    while (word == "" or not word[-1].isspace()) and len(word) < max_len:

        output = network.compute(format_one_hot_messages(message_to_one_hot(message + word)))[0]

        top_indices = np.argsort(output)[-CHOOSE_N_CANDIDATES_FROM_TOP:]
        top_probabilities = output[top_indices]
        normalized_probabilities = top_probabilities / top_probabilities.sum()
        selected = np.random.choice(top_indices, p=normalized_probabilities)

        char = num_to_lower_char(selected)

        word += char

    return word

# Tkinter application setup
class TextPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Text Predictor {NETWORK_PATH.name}")

        # Layout for text box and bar graph canvas
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        # Text input box
        self.text_box = tk.Text(self.frame, height=20, width=50)
        self.text_box.grid(row=0, column=0)

        # Canvas for bar graph
        self.canvas = tk.Canvas(self.frame, width=300, height=200, bg="white")
        self.canvas.grid(row=0, column=1, padx=20)

        # Label for predicted word
        self.predicted_word_label = tk.Label(self.frame, text="Next word prediction:", font=("Arial", 12))
        self.predicted_word_label.grid(row=1, column=0, sticky="w")

        self.update_prediction()

        # Bind text box to events
        self.text_box.bind("<KeyRelease>", self.update_prediction)
        self.text_box.bind("<Key>", self.key)

        # Predicted word state
        self.predicted_word = ""

    def key(self, event=None):        
        if event and event.char == "\t":
            self.text_box.insert(tk.END, self.predicted_word)
            return "break"

    def update_prediction(self, event=None):
        current_message = self.text_box.get("1.0", "end-1c")

        top_indices, probabilities = predict_next_character_probs(current_message)
        self.update_bar_graph(top_indices, probabilities)

        self.predicted_word = predict_next_word(current_message)
        self.predicted_word_label.config(text=f"Prediction: {repr(self.predicted_word)}")

    def update_bar_graph(self, top_indices, probabilities):
        # Clear previous graph
        self.canvas.delete("all")

        # Define bar graph dimensions
        bar_width = 20
        spacing = 10
        x_offset = 50
        max_height = 150

        # Draw the bar graph for the top 10 characters
        for i, (index, prob) in enumerate(zip(top_indices, probabilities)):
            char = num_to_lower_char(index)
            bar_height = max_height * prob
            x0 = i * (bar_width + spacing) + x_offset
            y0 = max_height - bar_height
            x1 = x0 + bar_width
            y1 = max_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
            self.canvas.create_text(x0 + bar_width / 2, y1 + 15, text=repr(char), font=("Arial", 10))

    def clear_bar_graph(self):
        self.canvas.delete("all")

# Initialize the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = TextPredictorApp(root)
    root.mainloop()
