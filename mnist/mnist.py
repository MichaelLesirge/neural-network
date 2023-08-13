import numpy as np

# from keras.datasets import mnist
# (X_train, y_train), (X_test, y_test) = mnist.load_data()

import tkinter as tk
root = tk.Tk()
root.title("MNIST Drawing Test")
root.resizable(width=False, height=False)

from matplotlib import pyplot as plt

def _draw_dot(array, row, col, value):
    array[row, col] = min(array[row, col] + ((1 - value) * 255), 255)

def draw_line(array, row1, column1, row2, column2):
    if any(x >= 28 for x in [row1, row2, column1, column2]): print([row1, row2, column1, column2])
    column_distance = abs(column1 - column2)

    row_distance = abs(row1 - row2)
    error = column_distance - row_distance
    last_error = 0
        
    column_change = 1 if column1 < column2 else -1
    row_change = 1 if row1 < row2 else -1

    distance_change = 1 if column_distance + row_distance == 0 else np.sqrt(column_distance*column_distance + row_distance*row_distance)

    current_column, current_row = column1, row1
    while True:
        _draw_dot(array, current_row, current_column, np.fabs(error - column_distance + row_distance) / distance_change)

        last_error = error
        last_column = current_column

        if 2 * last_error >= -column_distance:
            if current_column == column2:
                break
            if (last_error + row_distance) < distance_change:
                _draw_dot(array, current_row + row_change, current_column, np.fabs(last_error + row_distance) / distance_change)
            error -= row_distance
            current_column += column_change

        if 2 * last_error <= row_distance:
            if current_row == row2:
                break
            if (column_distance - last_error) < distance_change:
                _draw_dot(array, current_row, last_column + column_change, np.fabs(column_distance - last_error) / distance_change)
            error += column_distance
            current_row += row_change

class DrawingBoard:
    def __init__(self, canvas: tk.Canvas, save_size: tuple[int, int], on_update = lambda pixels:None) -> None:
        self.canvas = canvas
        self.canvas.config(cursor="crosshair")        
        self.canvas_width, self.canvas_height = self.canvas.winfo_reqheight(), self.canvas.winfo_reqwidth()
        
        self.pixel_array = np.zeros(save_size, dtype=int)
        
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.start_draw)
        
        self.on_update = on_update

        self.previous_draw_point = (None, None)
        
        self.clear_button = tk.Button(root, text="Clear Drawing", command=self.clear_canvas)
        
        self.show_button = tk.Button(root, text="Display Drawing Array", command=self.show_graph)
        
        self.pen_size = 10
    
    def is_in_canvas(self, x, y):
        return 0 < x < self.canvas_width and 0 < y < self.canvas_height
    
    def start_draw(self, event):
        self.previous_draw_point = (event.x, event.y)
        
        size = self.pen_size / 2
        self.canvas.create_oval(event.x+size, event.y+size, event.x-size, event.y-size, fill="black", tags="line")
        
        if self.is_in_canvas(event.x, event.y):
            row, col = self.scale_for_save(event.x, event.y)
            self.pixel_array[row, col] = 255
            
        self.on_update(self.pixel_array) 
            
    def draw(self, event): 
        prev_x, prev_y = self.previous_draw_point
        self.previous_draw_point = (event.x, event.y)

        self.canvas.create_line(event.x, event.y, prev_x, prev_y, fill="black", smooth=True, width=self.pen_size, tags="line")
                               
        if self.is_in_canvas(event.x, event.y) and self.is_in_canvas(prev_x, prev_y):
            row1, col1 = self.scale_for_save(event.x, event.y)
            row2, col2 = self.scale_for_save(prev_x, prev_y)
            draw_line(self.pixel_array, row1, col1, row2, col2)
         
        self.on_update(self.pixel_array) 
    
    def scale_for_save(self, x, y):
        row = round(y / self.canvas_width * np.size(self.pixel_array, 0)) - 1
        col = round(x / self.canvas_height * np.size(self.pixel_array, 1)) - 1
        return row, col

    def clear_canvas(self):
        self.pixel_array = np.zeros_like(self.pixel_array)
        self.canvas.delete("line")
    
    def show_graph(self):
        # print("\n | " + "--" * (np.size(self.pixel_array, 1)) + " | ")
        # greys = " .,*/(#%&@"
        # print("\n".join(" | " + (" ".join(greys[int((pixel / 255) * (len(greys)-1))] for pixel in row)) + "  | " for row in self.pixel_array))
        # print(" | " + "--" * (np.size(self.pixel_array, 1)) + " | \n")
        
        plt.imshow(self.pixel_array, cmap="Greys")
        plt.show()
        
    def pack_buttons(self, *args, **kwargs):
        self.clear_button.pack(*args, **kwargs)
        self.show_button.pack(*args, **kwargs)

class OutputsDisplay:
    def __init__(self, canvas) -> None:
        self.canvas = canvas

# small_drawing_size = X_train[0].shape
small_drawing_width, small_drawing_height = (28, 28)
large_drawing_width, large_drawing_height = (400, 400)

button_canvas = tk.Canvas(root, width=100)
button_canvas.pack(side="bottom", pady=10)

drawing_canvas = tk.Canvas(root, background="white", highlightbackground="grey", width=large_drawing_width, height=large_drawing_height)
drawing_canvas.pack(side="left", padx=10, pady=10)

info_canvas = tk.Canvas(root, width=200, height=large_drawing_height)
info_canvas.pack(side="left", padx=10, pady=10)

output_canvas = tk.Canvas(root, background="white", highlightbackground="grey", width=large_drawing_width, height=large_drawing_height)
output_canvas.pack(side="left", padx=10, pady=10)

def update(pixels): 
    output = [[0.1, 0.1, 0, 0, 0, 0, 0.2, 0.6, 0, 0]][0]
    guess = np.argmax(output)
    
    output_canvas.create_text(large_drawing_width/2, large_drawing_height/2, justify='center', text=str(guess), font=("Arial", int(large_drawing_height * 0.5)))
    
    

drawing_board = DrawingBoard(drawing_canvas, (small_drawing_width, small_drawing_height), update)
drawing_board.pack_buttons(in_=button_canvas, side="left", padx=5)

root.mainloop()
