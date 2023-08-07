import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# --- back propagation hyper parameters ---

EPOCHS = 2
BATCH_SIZE = 4
LEARNING_RATE = 0.01

# --- function parameters  ---

noise_level = 0.1
m, b = 0.5, 0.2

def f(x, *, m=1, b=0, variation=0):
    return (m * x + b) + (np.random.randn(*x.shape) * variation)

# --- create train and test data ---

train_size = 2**9

# x_train = np.random.randn(x_train_size, 1)
x_train = np.random.uniform(-2, 2, (train_size, 1))
y_train = f(x_train, variation=noise_level, m=m, b=b)

# --- initialize weights and biases ---

input_size, output_size = 1, 1

# each row of weights aligns with one input, each column with one output (view example_forward_pass.py)
weights = np.random.randn(input_size, output_size)
# weights = np.array([[-0.7]])

# bias for each output neuron
bias = np.zeros((1, output_size), np.float64)

# ---errors ---

def mse(y_true, y_pred):
    return np.mean(np.square(y_true - y_pred))

def mse_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / np.size(y_true, 0)

# --- training ---

def n_split_array(arr, n_size, *, keep_extra=True):
    """split arr into chunks of size n with extra added on end if keep_extra is true"""
    if n_size is None: return arr
    div, extra = divmod(np.size(arr, 0), n_size)
    a, b = np.split(arr, [extra]) if extra else arr, None
    return np.array_split(a, div) + ([b] if (b and keep_extra) else [])


def same_shuffle(arrays):
    """shuffle 2 arrays """
    order = np.arange(np.size(arrays[0], 0))
    np.random.shuffle(order)
    return tuple(array[order] for array in arrays)

losses_history = []
params_history = []
x_batches_history, y_batches_history = [], []

for epoch in range(EPOCHS):
    x_train, y_train = same_shuffle((x_train, y_train))
    for x_batch, y_batch in zip(n_split_array(x_train, BATCH_SIZE, keep_extra=False), n_split_array(y_train, BATCH_SIZE, keep_extra=False)):
        # --- forward pass of our one layer on batch ---
        output = np.dot(x_batch, weights) + bias
        loss = mse(y_batch, output)

        # --- backward pass ---
        loss_gradient = mse_prime(y_batch, output)
        
        weights_gradient = np.dot(x_batch.T, loss_gradient)
        weights += LEARNING_RATE * -weights_gradient

        bias_gradient = np.sum(loss_gradient, axis=0, keepdims=True)
        bias += LEARNING_RATE * -bias_gradient

        # output_gradient = np.dot(weights, batch_x.T)

        # --- save data for animation ---
        losses_history.append(loss)
        params_history.append((weights.copy(), bias.copy()))

        x_batches_history.extend(x_batch.flatten().tolist())
        y_batches_history.extend(y_batch.flatten().tolist())

total_runs = len(params_history)

# --- graph parameters ---

TITLE = "one neuron"
STYLE = "dark_background"
GRAPH_HEIGHT_RATIO = (4, 1)

# --- animation parameters ---

ANIMATION_FRAMES_PER_MS = 100
SHOW_TRUE_LINE_AT = -1

# --- animation / graphing ---
plt.style.use(STYLE)

figure, (dot_axis, loss_axis) = plt.subplots(2, gridspec_kw={"height_ratios": GRAPH_HEIGHT_RATIO})
figure.tight_layout()

dot_axis.set_title(f"{TITLE.title()} {EPOCHS=} {BATCH_SIZE=} {LEARNING_RATE=}")
dot_axis.set_xlim(left=np.min(x_train), right=np.max(x_train))
dot_axis.set_ylim(bottom=np.min(y_train), top=np.max(y_train))
(past_dots,) = dot_axis.plot([], [], "o", color="grey",  markersize=2, label="past")
(current_dots,) = dot_axis.plot([], [], "o", color="red",  markersize=4, label="batch")

(pred_line,) = dot_axis.plot([], [], markersize=3, label="pred")
(true_line,) = dot_axis.plot([], [], color="green", markersize=3, label="true")
dot_axis.legend(loc="lower right")

loss_axis.set_title("Loss")
loss_axis.set_xlim(left=0, right=total_runs)
loss_axis.set_ylim(bottom=0, top=max(losses_history))
(loss_line,) = loss_axis.plot([], [], label="loss")

animation_lines = [past_dots, current_dots, pred_line, true_line, loss_line]

batches_per_epoch = train_size // BATCH_SIZE

def init():
    for line in animation_lines:
        line.set_data([], [])
        line.set_animated(True)
    return animation_lines

def update(i):
    losses = losses_history[:i+1]
    loss_line.set_data(range(i+1), losses)
        
    if i >= total_runs + SHOW_TRUE_LINE_AT:
        true_line.set_data(x_train, m * x_train + b)
    
    epoch_start = (i // batches_per_epoch) * batches_per_epoch
    
    past_points_x, past_points_y = x_batches_history[epoch_start:i], y_batches_history[epoch_start:i]
    past_dots.set_data(past_points_x, past_points_y)
    
    current_batch_x, current_batch_y = x_batches_history[i:i+BATCH_SIZE], y_batches_history[i:i+BATCH_SIZE]
    current_dots.set_data(current_batch_x, current_batch_y)
    
    weights, biases = params_history[i] 
    pred_line.set_data(x_train, np.dot(x_train, weights) + biases)
    
    
    return animation_lines

animation = FuncAnimation(figure, update, frames=total_runs, init_func=init, blit=True, interval=ANIMATION_FRAMES_PER_MS, repeat=False)
figure_manager = plt.get_current_fig_manager()
plt.show()

# save = input("Save (y/N): ").lower().strip() in ("y", "yes", "true")
# if save: animation.save("one_neuron_back_prop.gif")