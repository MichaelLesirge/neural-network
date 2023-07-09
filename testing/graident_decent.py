import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

def y_func(x): return 0.1 * x ** 2
# def y_func(x): return np.sin(0.5 * x) + 0.3 * np.sin(2 * x) + 0.2 * x

def mean_squared_error(predicted, target):
    return np.mean(np.square(predicted - target))    

x_min_max, step = 10, 0.1
x_data = np.arange(-x_min_max, x_min_max + step, step)
y_data = y_func(x_data)

y_target = 0

"""
TODO:
Fix  MatplotlibDeprecationWarning: dots.set_data(point) by using scatter or something, not a hacky way
Add percentage done on animation printout
Add error threshold use
"""

learning_rate = 0.01
error_threshold = 0.0001

positions_and_errors = []

max_iterations = 5000 + 1

x = np.random.choice(x_data)
 
for i in range(max_iterations):
    y = y_func(x)
    
    error = mean_squared_error(y, y_target)
    positions_and_errors.append(((x, y), error))
    
    error_delta = mean_squared_error(y_func(x + 0.00001), y_target)
    gradient = (error_delta - error) / 0.00001
    
    x += learning_rate * -gradient


# --- Plotting stuff ---

error_figure, error_axis = plt.subplots()
error_figure.suptitle("Error")
error_axis.plot([error for position, error in positions_and_errors ], label = "Error")
error_axis.legend(loc="best")

figure, axis = plt.subplots()
figure.suptitle("Gradient Descent Animation")
axis.plot(x_data, y_data, label="Line")
(dots,) = axis.plot([], [], "ro", label="Point")
axis.legend(loc="best")


def init():
    dots.set_data([], [])
    return (dots,)

print_step = 100
def update(n_frame):
    global last
    
    point, error = positions_and_errors[n_frame]
    
    dots.set_data(point)
    
    if (n_frame % print_step == 0):
        last_point, last_error = positions_and_errors[max(n_frame - print_step, 0)]
        print(f"#{n_frame}: {point=}, {error=}. {(last_error - error) / last_error:%} better than last")
    
    return (dots,)

animation = FuncAnimation(figure, update, frames=len(positions_and_errors), init_func=init, blit=True, interval=0.001, repeat=False)

plt.show()
