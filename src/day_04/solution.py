from typing import Iterable, Iterator


def to_range(s: str) -> range:
    start, stop = map(int, s.split("-"))
    return range(start, stop + 1)


def parse_input(filename: str) -> Iterator[tuple[range, range]]:
    try:
        f = open(filename)
    except OSError as err:
        print(f"Couldn't open file {filename}. Error: {err}")
    else:
        with f:
            for line in f:
                line = line.strip()
                if len(pair := line.split(",")) == 2:
                    yield tuple(map(to_range, pair))


def find_overlap(a: range, b: range) -> range:
    start_a, stop_a = a[0], a[-1]
    start_b, stop_b = b[0], b[-1]
    left_boundary = max(start_a, start_b)
    right_boundary = min(stop_a, stop_b)
    if left_boundary > right_boundary:
        return range(0)
    return range(left_boundary, right_boundary + 1)


def solution_1(sections: Iterable[tuple[range, range]]) -> int:
    score = 0
    for pair in sections:
        overlap = find_overlap(*pair)
        if any(section == overlap for section in pair):
            score += 1
    return score


def solution_2(sections: Iterable[tuple[range, range]]) -> int:
    return sum(1 for pair in sections if find_overlap(*pair))


def main() -> None:
    assert solution_1(parse_input("input_example")) == 2
    print(solution_1(parse_input("input")))
    assert solution_2(parse_input("input_example")) == 4
    print(solution_2(parse_input("input")))


if __name__ == "__main__":
    main()
