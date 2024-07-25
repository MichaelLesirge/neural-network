from util import *

def main() -> None:
    CHOOSE_FROM_TOP = 2

    network.load(str(directory / "mass-train" / "char-network-v0"))

    if CHOOSE_FROM_TOP is None:
        print("Choose next character based on random choice with probabilities")
    elif CHOOSE_FROM_TOP == 1:
        print("Choose next character based on highest probability")
    else:
        print(f"Choose next character based on random choice from top {CHOOSE_FROM_TOP} with probabilities")
    print()    

    while True:
        message = input("CharGPN> ")

        print(message, end="")

        while len(message) == 0 or message[-1] not in TERMINATION_CHARS:
            output = network.compute(format_one_hot_messages(message_to_one_hot(message)))[0]

            top_indices = np.argsort(output)[-(CHOOSE_FROM_TOP if CHOOSE_FROM_TOP is not None else len(output)):]
            top_probabilities = output[top_indices]
            normalized_probabilities = top_probabilities / top_probabilities.sum()
            selected = np.random.choice(top_indices, p=normalized_probabilities)

            char = num_to_lower_char(selected)
            print(char, end="")

            message += char
        print()

if __name__ == "__main__":
    main()