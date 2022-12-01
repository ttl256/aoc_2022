from typing import Iterator, Sequence


def parse_input(filename: str) -> Iterator[int]:
    try:
        f = open(filename)
    except OSError as err:
        print(f"Couldn't open file {filename}. Error: {err}")
    else:
        with f:
            buffer: list[str] = []
            for line in f:
                line = line.strip()
                if line:
                    buffer.append(line)
                else:
                    yield sum(map(int, buffer))
                    buffer.clear()
            if buffer:
                yield sum(map(int, buffer))


def solution_1(calories: Sequence[int]) -> int:
    return calories[0]


def solution_2(calories: Sequence[int]) -> int:
    return sum(calories[:3])


def main() -> None:
    input_example = sorted(list(parse_input("input_example")), reverse=True)
    input_ = sorted(list(parse_input("input")), reverse=True)
    assert solution_1(input_example) == 24000
    print(solution_1(input_))
    assert solution_2(input_example) == 45000
    print(solution_2(input_))


if __name__ == "__main__":
    main()
