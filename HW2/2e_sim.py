from random import randint
from typing import List


def update(state_history: List[int]) -> List[int]:
    new_state_history = state_history.copy()

    new_state = "G" if randint(0, 1) == 0 else "R"
    new_state_history.append(new_state)

    return new_state_history


def main():
    STEPS = 37
    history = []
    for i in range(STEPS):
        history = update(history)

    print(history)

    RED_COUNT = history.count("R")
    GREEN_COUNT = history.count("G")

    print(f"RED COUNT {RED_COUNT}")
    print(f"GREEN COUNT {GREEN_COUNT}")


if __name__ == "__main__":
    main()
