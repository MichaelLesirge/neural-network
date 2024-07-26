from network_util import *

# How many candidates to consider for next character, chooses from highest ranked charters.
# If this value is one, then only the highest ranked character is over picked
# If a number is picked it will pick that many (N) highest ranked numbers
# You can set to util.NUMBER_OF_CHARS_IN_RANGE to make every result a candidate
# Treat this like "temperature" of creativity
CHOOSE_N_CANDIDATES_FROM_TOP = 2

# From the pool of candidates, whether the ranks should be considered when a choice is made
# If this is True, higher ranked caudates have a higher chance of being picked
# If False, all caudates are treated equally
USE_PROBABILITIES = True

# Path to saved network weights and biases. You do not need to include file extension

NETWORK_PATH = directory / "char-network-b"
# NETWORK_PATH = directory / "looped-train" / "char-network-v0"

def main() -> None:
     
    print(f"Loading network from {NETWORK_PATH}")
    
    network.load(str(NETWORK_PATH))

    if CHOOSE_N_CANDIDATES_FROM_TOP is None: 
        print(f"Choose next character based on random choice", "with probabilities" if USE_PROBABILITIES else "")
    elif CHOOSE_N_CANDIDATES_FROM_TOP == 1:
        print(f"Choose next character based on highest probability.")
    else:
        print(f"Choose next character based on random choice from top {CHOOSE_N_CANDIDATES_FROM_TOP}", "with probabilities." if USE_PROBABILITIES else "")
    print()    

    while True:
        message = input("CharGPN> ")

        print(message, end="")

        # while (len(message) == 0 or message[-1] not in TERMINATION_CHARS) and (message.count(".") < 3):
        # while (len(message) == 0 or message.count(END_LINE) < 3):
        # while (len(message) == 0 or message[-1] not in TERMINATION_CHARS):
        while (len(message) < 2 or message[-2] not in ".\n"):
            output = network.compute(format_one_hot_messages(message_to_one_hot(message)))[0]

            top_indices = np.argsort(output)[-(CHOOSE_N_CANDIDATES_FROM_TOP if CHOOSE_N_CANDIDATES_FROM_TOP is not None else len(output)):]
            top_probabilities = output[top_indices]
            normalized_probabilities = top_probabilities / top_probabilities.sum()
            selected = np.random.choice(top_indices, p=normalized_probabilities)

            char = num_to_lower_char(selected)
            print(char, end="")

            message += char

        print("\n")

if __name__ == "__main__":
    main()