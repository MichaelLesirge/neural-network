import tkinter as tk

import numpy as np
from keras.datasets.mnist import load_data
from matplotlib import pyplot as plt

import neural_network as nn

# --- get data and set constants ---

(X_train, y_train), (X_test, y_test) = load_data()

small_drawing_width, small_drawing_height = X_train[0].shape
large_drawing_width, large_drawing_height = (400, 400)

n_inputs, n_outputs = small_drawing_width * small_drawing_height, max(y_train.max(), y_train.max()) + 1
layer_size = 2**5

# --- Define neural network and get params for it ---


def preprocess(inputs):
    return inputs.astype(np.float64) / 255


network = nn.network.Network([
    nn.layers.Reshape((small_drawing_width, small_drawing_height), (n_inputs,)),

    nn.layers.Dense(n_inputs, layer_size),
    nn.activations.ReLU(),

    nn.layers.Dense(layer_size, n_outputs),
    nn.activations.Softmax(),

], loss=nn.losses.CategoricalCrossEntropy(categorical_labels=True), preprocess=[preprocess])


try:
    network.load_params("mnist-network")
except FileNotFoundError:
    print("\nStarting Training...")

    network.train(X_train, y_train, batch_size=16, epochs=2, learning_rate=0.1)
    network.save_params("mnist-network")

# --- test model on test data ---

test_output = network.compute(X_test)

predictions = test_output.argmax(1)
accuracy = np.mean(predictions == y_test)

print("\nDisplaying tests...")
for num in range(0, n_outputs):
    index = np.random.choice(np.where(y_test == num)[0])
    output = test_output[index]
    guess = output.argmax()

    print(f"y_pred={output.tolist()}, y_true={np.eye(n_outputs)[guess]}")

    plt.title(
        f"Test Data Example {num}:\n{guess=}, confidence={output[guess]:.2%}, correct={guess==num}")
    plt.imshow(X_test[index], cmap="Greys")
    plt.show()

print(f"{accuracy:%} accurate on test data")

# --- create drawing GUI ---

root = tk.Tk()
root.title("MNIST Drawing Test")
root.resizable(width=False, height=False)


def draw_dot(array: np.ndarray, row: int, col: int, value: float) -> None:
    if -1 < row < np.size(array, 1) and -1 < col < np.size(array, 0):
        array[row, col] = min(array[row, col] + ((1 - value) * 255), 255)


def draw_blob(array, row, col, value):
    draw_dot(array, row, col, value)

    value_edge = 1 - (1-value) / 5
    draw_dot(array, row+1, col, value_edge)
    draw_dot(array, row, col+1, value_edge)
    draw_dot(array, row-1, col, value_edge)
    draw_dot(array, row, col-1, value_edge)

    value_corner = 1 - (1-value) / 10
    draw_dot(array, row+1, col+1, value_corner)
    draw_dot(array, row-1, col+1, value_corner)
    draw_dot(array, row+1, col-1, value_corner)
    draw_dot(array, row-1, col-1, value_corner)


def draw_line(array: np.ndarray, row1: int, col1: int, row2: int, col2: int):
    col_distance = abs(col1 - col2)

    row_distance = abs(row1 - row2)
    error = col_distance - row_distance
    last_error = 0

    col_change = 1 if col1 < col2 else -1
    row_change = 1 if row1 < row2 else -1

    distance_change = 1 if col_distance + row_distance == 0 else \
        np.sqrt(col_distance*col_distance + row_distance*row_distance)

    current_col, current_row = col1, row1
    while True:
        draw_blob(array, current_row, current_col,
                  np.abs(error - col_distance + row_distance) / distance_change)

        last_error = error
        last_col = current_col

        if 2 * last_error >= -col_distance:
            if current_col == col2:
                break
            if (last_error + row_distance) < distance_change:
                draw_blob(array, current_row + row_change, current_col,
                          np.abs(last_error + row_distance) / distance_change)
            error -= row_distance
            current_col += col_change

        if 2 * last_error <= row_distance:
            if current_row == row2:
                break
            if (col_distance - last_error) < distance_change:
                draw_blob(array, current_row, last_col + col_change,
                          np.abs(col_distance - last_error) / distance_change)
            error += col_distance
            current_row += row_change


class DrawingDisplay:
    def __init__(self, canvas: tk.Canvas, save_size: tuple[int, int], on_update=lambda pixels: None, on_reset=lambda: None) -> None:
        self.canvas = canvas
        self.canvas.config(cursor="crosshair")
        self.canvas_width, self.canvas_height = self.canvas.winfo_reqheight(), self.canvas.winfo_reqwidth()

        self.pixel_array = np.zeros(save_size, dtype=int)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.start_draw)

        self.on_update = on_update
        self.on_reset = on_reset

        self.previous_draw_point = (None, None)

        self.clear_button = tk.Button(
            root, text="Clear Drawing", command=self.clear_canvas)

        self.show_button = tk.Button(
            root, text="Display Drawing From Computers View", command=self.show_graph)

        self.pen_size = 5

    def start_draw(self, event: tk.Event) -> None:
        self.previous_draw_point = (event.x, event.y)

        size = self.pen_size / 2
        self.canvas.create_oval(
            event.x+size, event.y+size, event.x-size, event.y-size, fill="black", tags="line")

        row, col = self.scale_for_save(event.x, event.y)
        draw_blob(self.pixel_array, row, col, 0)

        self.on_update(self.pixel_array)

    def draw(self, event: tk.Event) -> None:
        prev_x, prev_y = self.previous_draw_point
        self.previous_draw_point = (event.x, event.y)

        self.canvas.create_line(event.x, event.y, prev_x, prev_y,
                                fill="black", smooth=True, width=self.pen_size)

        row1, col1 = self.scale_for_save(event.x, event.y)
        row2, col2 = self.scale_for_save(prev_x, prev_y)
        draw_line(self.pixel_array, row1, col1, row2, col2)

        self.on_update(self.pixel_array)

    def scale_for_save(self, x: float, y: float) -> tuple[int, int]:
        row = round(y / self.canvas_width * (np.size(self.pixel_array, 0) - 1))
        col = round(x / self.canvas_height *
                    (np.size(self.pixel_array, 1) - 1))
        return row, col

    def clear_canvas(self) -> None:
        self.pixel_array = np.zeros_like(self.pixel_array)
        self.canvas.delete(tk.ALL)
        self.on_reset()

    def show_graph(self) -> None:
        plt.imshow(self.pixel_array, cmap="Greys")
        print("\n".join((" ".join(str(pixel).ljust(3) for pixel in row)) for row in self.pixel_array), "\n")
        plt.show()

    def place_buttons(self) -> None:
        button_canvas = tk.Canvas(self.canvas)
        button_canvas.place(in_=self.canvas, relx=0.0, rely=1.0)

        self.clear_button.pack(in_=button_canvas, side="left", padx=5, pady=5)
        self.show_button.pack(in_=button_canvas, side="left", padx=5, pady=5)


class NetworkInfoDisplay:
    def __init__(self, canvas: tk.Canvas, n_neurons: int) -> None:
        self.canvas = canvas

        self.sub_canvas_size = 40

        self.n_neurons = n_neurons

        self.neuron_canvases = [tk.Canvas(
            self.canvas, width=self.sub_canvas_size, height=self.sub_canvas_size) for n in range(self.n_neurons)]
        self.percent_canvases = [tk.Canvas(
            self.canvas, width=self.sub_canvas_size*1.5, height=self.sub_canvas_size) for n in range(self.n_neurons)]

        for index, item in enumerate(self.neuron_canvases):
            item.grid(column=0, row=index, pady=3)
        for index, item in enumerate(self.percent_canvases):
            item.grid(column=1, row=index, pady=3)

    def update(self, outputs: np.ndarray):
        for index, (output, neuron_canvas, percent_canvas) in enumerate(zip(outputs, self.neuron_canvases, self.percent_canvases)):
            brightness = int((1-output) * 255)

            neuron_canvas.delete(tk.ALL)
            neuron_canvas.create_oval(3, 3, self.sub_canvas_size, self.sub_canvas_size, outline="black",
                                      offset="n", fill="#%02x%02x%02x" % (brightness, brightness, brightness))
            neuron_canvas.create_text(self.sub_canvas_size/1.9, self.sub_canvas_size/1.9,
                                      fill=("white" if brightness < 200 else "black"), text=str(index), justify="center", font=("Arial", int(self.sub_canvas_size * 0.25)))

            percent_canvas.delete(tk.ALL)
            percent_canvas.create_text(self.sub_canvas_size/1.9, self.sub_canvas_size/1.9,
                                       text=format(output, ".0%"), justify="center", font=("Arial", int(self.sub_canvas_size * 0.25)))

    def reset(self):
        self.update(np.zeros(self.n_neurons))


class GuessDisplay:
    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas

    def update(self, outputs: np.ndarray):
        guess = outputs.argmax()
        confidence = outputs[guess]

        # made by ChatGPT
        confidence_levels = [
            "I'm completely clueless about this, maybe it's a",
            "I really can't say for sure, perhaps it's a",
            "I have no strong feelings, but maybe it's a",
            "I'm not entirely sure, but it could be a",
            "I'm not too confident, but maybe a",
            "It's a wild guess, but maybe a",
            "I have a slight inkling, it might be a",
            "I'm leaning towards this, it could be a",
            "I'm somewhat confident, it might be a",
            "I'm not fully convinced, but possibly a",
            "I'm moderately confident, it could be a",
            "I'm getting more certain, it might be a",
            "I'm fairly confident, it's likely a",
            "I'm feeling quite sure, it could be a",
            "I'm fairly certain, it might be a",
            "I'm pretty confident, it seems to be a",
            "I'm quite sure, it's probably a",
            "I'm almost certain, it could be a",
            "I'm highly confident, it's very likely a",
            "I'm nearly 100% sure, it must be a",
            "That's obviously a",
        ]

        self.canvas.delete(self.canvas.delete(tk.ALL))

        smallest_max = 1 / len(outputs)
        self.canvas.create_text(large_drawing_width/2, large_drawing_height/10, justify="center",
                                text=confidence_levels[int((confidence - smallest_max) / (1 - smallest_max) * (len(confidence_levels) - 1))],
                                font=("Arial", int(large_drawing_height * 0.03)))

        self.canvas.create_text(large_drawing_width/2, large_drawing_height/2, justify="center",
                                text=str(guess),
                                font=("Arial", int(large_drawing_height * 0.5)))
        # self.canvas.create_text(large_drawing_width/2, large_drawing_height - large_drawing_height/10, justify="center",
        #                         text=format(confidence, "%"))

    def reset(self):
        self.canvas.delete(tk.ALL)


drawing_canvas = tk.Canvas(root, background="white", highlightbackground="grey",
                           width=large_drawing_width, height=large_drawing_height)
drawing_canvas.grid(row=0, column=0, padx=10, pady=10)

network_info_canvas = tk.Canvas(root, width=20, height=large_drawing_height)
network_info_canvas.grid(row=0, column=1, padx=10, pady=10)

network_info = NetworkInfoDisplay(network_info_canvas, n_outputs)

guess_canvas = tk.Canvas(root, background="white", highlightbackground="grey",
                         width=large_drawing_width, height=large_drawing_height)
guess_canvas.grid(row=0, column=2, padx=10, pady=10)
guess_info = GuessDisplay(guess_canvas)


def reset():
    guess_info.reset()
    network_info.reset()


def update(pixels: np.ndarray):
    # do neural network stuff here
    output = network.compute(np.array([pixels]))[0]
    network_info.update(output)
    guess_info.update(output)


drawing_board = DrawingDisplay(
    drawing_canvas, (small_drawing_width, small_drawing_height), update, reset)
drawing_board.place_buttons()

reset()

print("\nDisplaying drawing demo.")
root.mainloop()
