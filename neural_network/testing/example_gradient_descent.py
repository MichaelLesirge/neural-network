import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# def f(x): return np.sin(0.5 * x) + 0.3 * np.sin(2 * x) + 0.2 * x
def f(x): return 0.1 * x ** 2

def mean_squared_error(predicted, target):
    return np.mean(np.square(predicted - target))    

def calculate_error(x, target):
    predicted = f(x)
    error = mean_squared_error(predicted, target)
    return error 

def gradient_descent(target, *, learning_rate=0.01, num_iterations=1000, start_x = 0):
    xs = []
    errors = []
    
    x = start_x
    for _ in range(num_iterations):
        error, gradient = error_derivative(x, target)
        x -= learning_rate * gradient
        
        xs.append(x)
        errors.append(error)

    return errors, xs

def error_derivative(x, target, delta=1e-5):
    error1 = calculate_error(x, target)
    error2 = calculate_error(x + delta, target)
    gradient = (error2 - error1) / delta
    return error1, gradient

def main() -> None:
    x_min, x_max = -10, 10

    x_vals = np.linspace(x_min, x_max, 10000)
    y_vals = f(x_vals)

    start_x = np.random.randint(x_min+1, x_max-1)
    target_y = np.min(y_vals)

    iterations = 5000 + 1
    
    errors, gradient_x_vals = gradient_descent(target=target_y, learning_rate=0.001, num_iterations=iterations, start_x=start_x)

    error_fig, error_axis = plt.subplots()
    error_fig.suptitle("Error")
    error_axis.plot(list(range(iterations)), errors, label = "Error")
    error_axis.legend(loc="best")
    
    dot_fig, dot_axis = plt.subplots()
    dot_fig.suptitle("Gradient Descent Animation")
    dot_axis.plot(x_vals, y_vals, label="Line")
    (dots,) = dot_axis.plot([], [], "ro", label="Point")
    dot_axis.legend(loc="best")

    def init():
        dots.set_data([], [])
        return (dots,)

    def update(frame):
        x = gradient_x_vals[frame]
        y = f(x)
        
        if (frame % 100 == 0):
            print(f"#{frame}: point={(x, y)}, error={errors[frame]}")
        dots.set_data([x], [y])
        
        return (dots,)

    anim = FuncAnimation(dot_fig, update, frames=iterations, init_func=init, blit=True, interval=0.1, repeat=False)

    plt.show()

if __name__ == "__main__":
    main()