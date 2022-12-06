from collections import deque
from typing import Any, Deque, Iterable, Iterator


def parse_input(filename: str) -> str:
    try:
        f = open(filename)
    except OSError as err:
        print(f"Couldn't open file {filename}. Error: {err}")
        return ""
    else:
        with f:
            return f.read()


def sliding_window(x: Iterable[Any], *, size: int) -> Iterator[tuple[list[Any], int]]:
    window: Deque[Any] = deque(maxlen=size)
    for idx, i in enumerate(x):
        # Prefill the window until it contains amount of items equal to its size
        window.append(i)
        if len(window) == size:
            yield list(window), idx


def first_nonrepeating_sequence(x: Iterable[Any], window_size: int) -> int:
    for window, idx in sliding_window(x, size=window_size):
        if len(set(window)) == window_size:
            return idx + 1
    return -1


def main() -> None:
    input_ = parse_input("input")
    input_example = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"

    # Part 1
    assert first_nonrepeating_sequence(input_example, 4) == 10
    print(first_nonrepeating_sequence(input_, 4))

    # Part 2
    assert first_nonrepeating_sequence(input_example, 14) == 29
    print(first_nonrepeating_sequence(input_, 14))

    # Fun. Is the solution general enough to work with any iterable?
    # Well, works with list of ints
    input_example_1 = [ord(i) for i in input_example]
    assert first_nonrepeating_sequence(input_example_1, 14) == 29


if __name__ == "__main__":
    main()
