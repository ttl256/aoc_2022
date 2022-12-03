from typing import Iterable, Iterator
from string import ascii_letters
import itertools
import functools


def parse_input_1(filename: str) -> Iterator[str]:
    try:
        f = open(filename)
    except OSError as err:
        print(f"Couldn't open file {filename}. Error: {err}")
    else:
        with f:
            for line in f:
                line = line.strip()
                yield line


def parse_input_2(x: Iterable[str]) -> Iterator[list[str]]:
    x = iter(x)
    while (chunk := list(itertools.islice(x, 3))) != []:
        yield chunk


def find_common_type_1(content: str) -> str:
    return (
        set(content[: len(content) // 2])
        .intersection(set(content[len(content) // 2 :]))
        .pop()
    )


def find_common_type_2(content: list[str]) -> str:
    return functools.reduce(
        lambda x, y: x.intersection(y), (set(i) for i in content)
    ).pop()


def solution_1(rucksacks_content: Iterable[str], priorities: dict[str, int]) -> int:
    score = 0
    for content in rucksacks_content:
        common_type = find_common_type_1(content)
        score += priorities[common_type]
    return score


def solution_2(
    rucksacks_content: Iterable[list[str]], priorities: dict[str, int]
) -> int:
    score = 0
    for i in rucksacks_content:
        common_type = find_common_type_2(i)
        score += priorities[common_type]
    return score


def main() -> None:
    priorities = dict(zip(ascii_letters, range(1, 53)))

    input_example_1 = list(parse_input_1("input_example"))
    input_1 = list(parse_input_1("input"))
    assert solution_1(input_example_1, priorities) == 157
    print(solution_1(input_1, priorities))

    input_example_2 = parse_input_2(input_example_1)
    input_2 = parse_input_2(input_1)
    assert solution_2(input_example_2, priorities) == 70
    print(solution_2(input_2, priorities))


if __name__ == "__main__":
    main()
