print("Loading modules...")

import pathlib
import sys

directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(directory.parent))

import tkinter as tk

import numpy as np
from matplotlib import pyplot as plt

import neural_network as nn
import data_saver

# --- get data and set constants ---

print("Loading data...")

# (X_train, y_train), (X_test, y_test) = load_data()

# small_drawing_width, small_drawing_height = X_train[0].shape
small_drawing_width, small_drawing_height = (28, 28) 
large_drawing_width, large_drawing_height = (400, 400)

# n_inputs, n_outputs = small_drawing_width * small_drawing_height, y_train.max() + 1
n_inputs, n_outputs = small_drawing_width * small_drawing_height, 10
layer_size = 2**8

# --- Define neural network and get params for it ---

def trim_zeros_2d(array: np.ndarray) -> np.ndarray:
    zeros = np.where(array != 0)
    if zeros[0].size == 0 or zeros[1].size == 0:
        return array
    min_row, max_row = np.min(zeros[0]), np.max(zeros[0])
    min_col, max_col = np.min(zeros[1]), np.max(zeros[1])
    return array[min_row:max_row+1, min_col:max_col+1]
    

def pad_to_square_2d(array: np.ndarray) -> np.ndarray:
    max_dim = max(array.shape)
    new_array = np.zeros((max_dim, max_dim), dtype=array.dtype)
    new_array[:array.shape[0], :array.shape[1]] = array
    return new_array

def interpolate_2d(array: np.ndarray, new_shape: tuple[int, int]) -> np.ndarray:
    new_array = np.zeros(new_shape, dtype=array.dtype)
    row_scale = new_shape[0] / array.shape[0]
    col_scale = new_shape[1] / array.shape[1]

    for i in range(new_shape[0]):
        for j in range(new_shape[1]):
            new_array[i, j] = array[int(i/row_scale), int(j/col_scale)]
    return new_array

def apply_all(arrays: np.ndarray, func, shape) -> np.ndarray:
    if arrays.ndim == 2:
        return func(arrays)
    if arrays.ndim == 3:
        new = np.ones(shape, dtype=arrays.dtype)
        for i, array in enumerate(arrays): new[i] = func(array)
        return new
    raise ValueError(f"Invalid number of dimensions: {arrays.ndim}")

def preprocess(inputs):
    inputs = inputs.astype(np.float64) / 255

    inputs = apply_all(inputs, lambda x: interpolate_2d(pad_to_square_2d(trim_zeros_2d(x)), (small_drawing_height, small_drawing_width)), (inputs.shape[0], small_drawing_width, small_drawing_height))

    return inputs

network = nn.network.Network([
    nn.layers.Reshape((small_drawing_width, small_drawing_height), (n_inputs,)),

    nn.layers.Dense(n_inputs, layer_size),
    nn.activations.ReLU(),

    nn.layers.Dense(layer_size, layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(layer_size, layer_size),
    nn.activations.ReLU(),
    
    nn.layers.Dense(layer_size, n_outputs),
    nn.activations.Softmax(),

], loss=nn.losses.CategoricalCrossEntropy(categorical_labels=True), preprocess=[preprocess])

save_file = str(directory / "mnist-network")
try:
    print(f"Attempting to load saved network from {save_file}...")
    network.load(save_file)
except FileNotFoundError:
    print("No saved network found, getting training data")
    
    (X_train, y_train), (X_test, y_test) = data_saver.load(directory)
     
    print("Starting Training...")
    network.train(X_train, y_train, batch_size=16, epochs=2, learning_rate=0.1)
    network.dump(save_file)

    # --- test model on test data ---

    test_output = network.compute(X_test)

    predictions = test_output.argmax(1)
    accuracy = np.mean(predictions == y_test)
    
    print(f"{accuracy:%} accurate on test data")

    # print("\nDisplaying tests...")
    # for num in range(0, n_outputs):
    #     index = np.random.choice(np.where(y_test == num)[0])
    #     output = test_output[index]
    #     guess = output.argmax()

    #     print(f"y_pred={output.tolist()}, y_true={np.eye(n_outputs)[guess]}")

    #     plt.title(
    #         f"Test Data Example {num}:\n{guess=}, confidence={output[guess]:.2%}, correct={guess==num}")
    #     plt.imshow(X_test[index], cmap="Greys")
    #     plt.show()

# --- create drawing GUI ---

def draw_dot(array: np.ndarray, row: int, col: int, value: float) -> None:
    if -1 < row < np.size(array, 1) and -1 < col < np.size(array, 0):
        array[row, col] = min(array[row, col] + ((1 - value) * 255), 255)

def draw_circle(array, row, col, value, radius=10, *, _pens={}) -> None:
    if radius not in _pens:
        x, y = np.indices((radius * 2 + 1, radius * 2 + 1))
        circle = np.sqrt((x - radius)**2 + (y - radius)**2) / np.sqrt(2 * radius**2)
        _pens[radius] = (1 - circle) * 255
    
    # array[row - radius:row + radius + 1, col - radius:col + radius + 1] = np.clip(
    #         array[row - radius:row + radius + 1, col - radius:col + radius + 1] + 
    #         _pens[radius].astype(array.dtype) * (1 - value), 0, 255)
    array[row - radius:row + radius + 1, col - radius:col + radius + 1] = np.maximum(
            array[row - radius:row + radius + 1, col - radius:col + radius + 1],
            _pens[radius].astype(array.dtype) * (1 - value))


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
        draw_circle(array, current_row, current_col,
                  np.abs(error - col_distance + row_distance) / distance_change)

        last_error = error
        last_col = current_col

        if 2 * last_error >= -col_distance:
            if current_col == col2:
                break
            if (last_error + row_distance) < distance_change:
                draw_circle(array, current_row + row_change, current_col,
                          np.abs(last_error + row_distance) / distance_change)
            error -= row_distance
            current_col += col_change

        if 2 * last_error <= row_distance:
            if current_row == row2:
                break
            if (col_distance - last_error) < distance_change:
                draw_circle(array, current_row, last_col + col_change,
                          np.abs(col_distance - last_error) / distance_change)
            error += col_distance
            current_row += row_change


class DrawingDisplay:
    def __init__(self, canvas: tk.Canvas, save_size: tuple[int, int] = None, on_update=lambda pixels: None, on_reset=lambda: None) -> None:
        self.canvas = canvas
        self.canvas.config(cursor="crosshair")
        self.canvas_width, self.canvas_height = self.canvas.winfo_reqheight(), self.canvas.winfo_reqwidth()

        if save_size is None:
            save_size = (self.canvas_height, self.canvas_width)
        self.pixel_array = np.zeros(save_size, dtype=int)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.start_draw)

        self.on_update = on_update
        self.on_reset = on_reset

        self.previous_draw_point = (None, None)

        self.buttons = [
            tk.Button(self.canvas.master, text="Clear Drawing", command=self.clear_canvas),
            tk.Button(self.canvas.master, text="Display Raw Data", command=self.show_graph),
            tk.Button(self.canvas.master, text="Display Processed Data", command=self.show_processed_graph),
        ]

        self.pen_size = 5

    def start_draw(self, event: tk.Event) -> None:
        self.previous_draw_point = (event.x, event.y)

        size = self.pen_size / 2
        self.canvas.create_oval(
            event.x+size, event.y+size, event.x-size, event.y-size, fill="black", tags="line")

        row, col = self.scale_for_save(event.x, event.y)
        draw_circle(self.pixel_array, row, col, 0)

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
        col = round(x / self.canvas_height * (np.size(self.pixel_array, 1) - 1))
        return row, col

    def clear_canvas(self) -> None:
        self.pixel_array = np.zeros_like(self.pixel_array)
        self.previous_draw_point = None
        self.canvas.delete(tk.ALL)
        self.on_reset()

    def show_graph(self) -> None:
        plt.imshow(self.pixel_array, cmap="Greys")
        plt.show()
        
    def show_processed_graph(self) -> None:
        plt.imshow(preprocess(self.pixel_array), cmap="Greys")
        plt.show()

    def place_buttons(self) -> None:
        button_canvas = tk.Canvas(self.canvas)
        button_canvas.place(in_=self.canvas, relx=0.0, rely=1.0)

        for button in self.buttons:
            button.pack(in_=button_canvas, side="left", padx=5, pady=5)


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

def main():
    root = tk.Tk()
    root.title("MNIST Drawing Test")
    root.resizable(width=False, height=False)
    
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

        # print(", ".join(f"{num}: {chance:.5%}" for num, chance in enumerate(output)))
        
        network_info.update(output)
        guess_info.update(output)


    drawing_board = DrawingDisplay(
        drawing_canvas, on_update=update, on_reset=reset)
    drawing_board.place_buttons()

    reset()

    print("\nDisplaying drawing demo.")
    root.mainloop()

if __name__ == "__main__":
    main()