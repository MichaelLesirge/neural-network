import tkinter as tk

import numpy as np
from matplotlib import pyplot as plt

# from keras.datasets import mnist
# (X_train, y_train), (X_test, y_test) = mnist.load_data()

root = tk.Tk()
root.title("MNIST Drawing Test")
root.resizable(width=False, height=False)


def draw_dot(array: np.ndarray, row: int, col: int, value: float) -> bool:
    if -1 < row < np.size(array, 1) and -1 < col < np.size(array, 0):
        array[row, col] = min(array[row, col] + ((1 - value) * 255), 255)


def draw_line(array: np.ndarray, row1: int, col1: int, row2: int, col2: int):
    col_distance = abs(col1 - col2)

    row_distance = abs(row1 - row2)
    error = col_distance - row_distance
    last_error = 0

    col_change = 1 if col1 < col2 else -1
    row_change = 1 if row1 < row2 else -1

    distance_change = 1 if col_distance + \
        row_distance == 0 else np.sqrt(col_distance*col_distance + row_distance*row_distance)

    current_col, current_row = col1, row1
    while True:
        draw_dot(array, current_row, current_col, np.fabs(
            error - col_distance + row_distance) / distance_change)

        last_error = error
        last_col = current_col

        if 2 * last_error >= -col_distance:
            if current_col == col2:
                break
            if (last_error + row_distance) < distance_change:
                draw_dot(array, current_row + row_change, current_col,
                         np.fabs(last_error + row_distance) / distance_change)
            error -= row_distance
            current_col += col_change

        if 2 * last_error <= row_distance:
            if current_row == row2:
                break
            if (col_distance - last_error) < distance_change:
                draw_dot(array, current_row, last_col + col_change,
                         np.fabs(col_distance - last_error) / distance_change)
            error += col_distance
            current_row += row_change


class DrawingBoard:
    def __init__(self, canvas: tk.Canvas, save_size: tuple[int, int], on_update=lambda pixels: None) -> None:
        self.canvas = canvas
        self.canvas.config(cursor="crosshair")
        self.canvas_width, self.canvas_height = self.canvas.winfo_reqheight(
        ), self.canvas.winfo_reqwidth()

        self.pixel_array = np.zeros(save_size, dtype=int)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.start_draw)

        self.on_update = on_update

        self.previous_draw_point = (None, None)

        self.clear_button = tk.Button(
            root, text="Clear Drawing", command=self.clear_canvas)

        self.show_button = tk.Button(
            root, text="Display Drawing Array", command=self.show_graph)

        self.pen_size = 5

    def start_draw(self, event: tk.Event) -> None:
        self.previous_draw_point = (event.x, event.y)

        size = self.pen_size / 2
        self.canvas.create_oval(
            event.x+size, event.y+size, event.x-size, event.y-size, fill="black", tags="line")

        row, col = self.scale_for_save(event.x, event.y)
        draw_dot(self.pixel_array, row, col, 0)

        self.on_update(self.pixel_array)

    def draw(self, event: tk.Event) -> None:
        prev_x, prev_y = self.previous_draw_point
        self.previous_draw_point = (event.x, event.y)

        self.canvas.create_line(event.x, event.y, prev_x, prev_y,
                                fill="black", smooth=True, width=self.pen_size, tags="line")

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
        self.canvas.delete("line")

    def show_graph(self) -> None:
        # print("\n | " + "--" * (np.size(self.pixel_array, 1)) + " | ")
        # greys = " .,*/(#%&@"
        # print("\n".join(" | " + (" ".join(greys[int((pixel / 255) * (len(greys)-1))] for pixel in row)) + "  | " for row in self.pixel_array))
        # print(" | " + "--" * (np.size(self.pixel_array, 1)) + " | \n")

        plt.imshow(self.pixel_array, cmap="Greys")
        plt.show()

    def place_buttons(self) -> None:
        button_canvas = tk.Canvas(self.canvas)
        button_canvas.place(in_=self.canvas, relx=0.0, rely=1.0)

        self.clear_button.pack(in_=button_canvas, side="left", padx=5, pady=5)
        self.show_button.pack(in_=button_canvas, side="left", padx=5, pady=5)


class OutputsDisplay:
    def __init__(self, canvas: tk.Canvas, n_neurons: int) -> None:
        self.canvas = canvas

        self.sub_canvas_size = 40

        self.neuron_canvases = [tk.Canvas(
            self.canvas, width=self.sub_canvas_size, height=self.sub_canvas_size) for n in range(n_neurons)]
        self.percent_canvases = [tk.Canvas(
            self.canvas, width=self.sub_canvas_size, height=self.sub_canvas_size) for n in range(n_neurons)]

        for index, item in enumerate(self.neuron_canvases):
            item.grid(column=0, row=index, pady=3)
        for index, item in enumerate(self.percent_canvases):
            item.grid(column=1, row=index, pady=3)

    def update_neurons(self, outputs: np.ndarray):
        for index, (output, neuron_canvas, percent_canvas) in enumerate(zip(outputs, self.neuron_canvases, self.percent_canvases)):

            brightness = int((1-output) * 255)
            neuron_canvas.create_oval(3, 3, self.sub_canvas_size, self.sub_canvas_size, outline="black", offset="n", fill='#%02x%02x%02x' % (brightness, brightness, brightness))
            neuron_canvas.create_text(self.sub_canvas_size/1.9, self.sub_canvas_size/1.9, text=str(index), justify="center", font=("Arial", int(self.sub_canvas_size * 0.25)))
            percent_canvas.delete('all')
            percent_canvas.create_text(self.sub_canvas_size/1.9, self.sub_canvas_size/1.9, text=format(output, ".1%"), justify="center", font=("Arial", int(self.sub_canvas_size * 0.25)))


# small_drawing_size = X_train[0].shape
small_drawing_width, small_drawing_height = (28, 28)
large_drawing_width, large_drawing_height = (300, 300)

drawing_canvas = tk.Canvas(root, background="white", highlightbackground="grey",
                           width=large_drawing_width, height=large_drawing_height)
drawing_canvas.grid(row=0, column=0, padx=10, pady=10)

info_canvas = tk.Canvas(root, width=20, height=large_drawing_height)
info_canvas.grid(row=0, column=1, padx=10, pady=10)

network_info = OutputsDisplay(info_canvas, 10)

output_canvas = tk.Canvas(root, background="white", highlightbackground="grey",
                          width=large_drawing_width, height=large_drawing_height)
output_canvas.grid(row=0, column=2, padx=10, pady=10)


def update(pixels: np.ndarray):
    # do neural network stuff here
    output = [[0.1, 0.1, 0, 0, 0, 0, 0.2, 0.6, 0, 0]][0]
    guess = np.argmax(output)

    output_canvas.create_text(large_drawing_width/2, large_drawing_height/2, justify='center',
                              text=str(guess), font=("Arial", int(large_drawing_height * 0.5)))
    network_info.update_neurons(output)


drawing_board = DrawingBoard(
    drawing_canvas, (small_drawing_width, small_drawing_height), update)
drawing_board.place_buttons()
network_info.update_neurons(np.zeros(10))

root.mainloop()
