from dataclasses import dataclass
import functools


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


@dataclass
class Node:
    coords: Coords
    v: int


class Grid(dict[Coords, Node]):
    def __init__(self, data: list[list[int]]):
        for idy, row in enumerate(data):
            for idx, val in enumerate(row):
                node = Node(Coords(idx, idy), val)
                self[node.coords] = node

        self.num_of_rows = max(coords.y for coords in self) + 1
        self.num_of_columns = max(coords.x for coords in self) + 1

    def neighbors(self, coords: Coords):
        return [
            list(reversed([Coords(i, coords.y) for i in range(0, coords.x + 1) if i != coords.x])),
            [Coords(i, coords.y) for i in range(coords.x, self.num_of_columns) if i != coords.x],
            list(reversed([Coords(coords.x, i) for i in range(0, coords.y + 1) if i != coords.y])),
            [Coords(coords.x, i) for i in range(coords.y, self.num_of_rows) if i != coords.y],
        ]

    def is_visible(self, coords: Coords) -> bool:
        if coords.x in (0, self.num_of_columns - 1) or coords.y in (0, self.num_of_rows - 1):
            return True
        node = self[coords]
        for direction in self.neighbors(coords):
            if all(self[neighbor].v < node.v for neighbor in direction):
                return True
        return False

    def scenic_score(self, coords: Coords) -> int:
        node = self[coords]
        scenic_score_per_direction: list[int] = []
        for direction in self.neighbors(coords):
            direction_score = 0
            if not direction:
                scenic_score_per_direction.append(direction_score)
            for idx, neighbor in enumerate(direction):
                neighbor_node = self[neighbor]
                if neighbor_node.v < node.v or idx == len(direction) - 1:
                    direction_score += 1
                elif neighbor_node.v >= node.v:
                    direction_score += 1
                    break
            scenic_score_per_direction.append(direction_score)
        return functools.reduce(lambda x, y: x * y, scenic_score_per_direction, 1)


    def __str__(self) -> str:
        return "\n".join(
            ("".join(str(self[Coords(j, i)].v) for j in range(self.num_of_columns)))
            for i in range(self.num_of_rows)
        )


def parse_input(filename: str) -> list[list[int]]:
    try:
        f = open(filename)
    except OSError as err:
        print(f"Couldn't open file {filename}. Error: {err}")
        return []
    else:
        with f:
            return [[int(char) for char in line.strip()] for line in f if line.strip()]


def part_1(grid: Grid) -> int:
    return sum(1 for coords, _ in grid.items() if grid.is_visible(coords))


def part_2(grid: Grid) -> int:
    return max(grid.scenic_score(coords) for coords, _ in grid.items())


def main() -> None:
    grid_example = Grid(parse_input("input_example"))
    grid = Grid(parse_input("input"))
    print(part_1(grid_example))
    print(part_2(grid_example))
    print(part_1(grid))
    print(part_2(grid))


if __name__ == "__main__":
    main()
