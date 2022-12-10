from typing import Callable, Iterator, Any
from enum import Enum, auto
from dataclasses import dataclass
from operator import add, sub


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    LEFT_UP = auto()
    LEFT_DOWN = auto()
    RIGHT_DOWN = auto()
    RIGHT_UP = auto()

@dataclass
class Coords:
    x: int
    y: int


@dataclass
class Move:
    direction: Direction
    amount: int


class Knot:
    def __init__(self, x: int, y: int):
        self.coords = Coords(x, y)

    def move(self, move: Move) -> None:
        dir_line: dict[Direction, tuple[str, Callable[[Any, Any], Any]]] = {
            Direction.LEFT: ("x", sub),
            Direction.RIGHT: ("x", add),
            Direction.UP: ("y", add),
            Direction.DOWN: ("y", sub),
        }
        dir_diagonal: dict[Direction, tuple[Direction, Direction]] = {
            Direction.LEFT_UP: (Direction.LEFT, Direction.UP),
            Direction.LEFT_DOWN: (Direction.LEFT, Direction.DOWN),
            Direction.RIGHT_UP: (Direction.RIGHT, Direction.UP),
            Direction.RIGHT_DOWN: (Direction.RIGHT, Direction.DOWN),
        }
        if move.direction in (Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN):
            setattr(
                self.coords,
                dir_line[move.direction][0],
                getattr(self.coords, dir_line[move.direction][0])
                + dir_line[move.direction][1](0, move.amount),
            )
        else:
            for dir in dir_diagonal[move.direction]:
                setattr(
                    self.coords,
                    dir_line[dir][0],
                    getattr(self.coords, dir_line[dir][0])
                    + dir_line[dir][1](0, move.amount),
                )

class Head(Knot):
    ...


class Tail(Knot):
    def __init__(self, x: int, y: int, head: Knot) -> None:
        super().__init__(x, y)
        self.head = head

    def is_touching(self) -> bool:
        my_c = (self.coords.x, self.coords.y)
        head_c = (self.head.coords.x, self.head.coords.y)
        return all(abs(a - b) < 2 for a, b in zip(my_c, head_c))

    def is_same_line(self) -> bool:
        return self.coords.x == self.head.coords.x or self.coords.y == self.head.coords.y

    def chase_on_line(self) -> Move:
        diff = (self.head.coords.x - self.coords.x, self.head.coords.y - self.coords.y)
        if diff == (2, 0): return Move(Direction.RIGHT, 1)
        if diff == (-2, 0): return Move(Direction.LEFT, 1)
        if diff == (0, 2): return Move(Direction.UP, 1)
        if diff == (0, -2): return Move(Direction.DOWN, 1)
        raise AssertionError("We shouldn't be here")

    def move_diagonally(self) -> Move:
        d = {
            (-1, 1): Direction.LEFT_UP,
            (-1, -1): Direction.LEFT_DOWN,
            (1, 1): Direction.RIGHT_UP,
            (1, -1): Direction.RIGHT_DOWN,
        }
        for (x, y), dir in d.items():
            # print(x, y, dir)
            new_tail = Tail(self.coords.x + x, self.coords.y + y, self.head)
            # print(f"{new_tail.coords=}")
            if new_tail.is_touching():
                # print(dir)
                return Move(dir, 1)


    def generate_move(self) -> Move:
        # Don't move if head and tail are adjecent
        if self.is_touching():
            return Move(Direction.LEFT, 0)
        if self.is_same_line():
            return self.chase_on_line()
        return self.move_diagonally()


class Rope:
    def __init__(self, num_of_knots: int) -> None:
        self.knots: list[Knot] = []
        for i in range(num_of_knots):
            if i == 0:
                self.knots.append(Head(x=0, y=0))
            else:
                self.knots.append(Tail(x=0, y=0, head=self.knots[i-1]))
        # print(self.knots)
        self.head = self.knots[0]
        self.tail = self.knots[-1]
        self.moves: set[tuple[int, int]] = set()

    def _move(self, move: Move) -> None:
        self.head.move(move)
        for knot in self.knots[1:]:
            new_move = knot.generate_move()
            knot.move(new_move)
            self.moves.add((self.tail.coords.x, self.tail.coords.y))
        # print(f"{self.head.coords=}")
        # print(f"{self.tail.coords=}")
        # print()

    def move(self, move: Move) -> None:
        # print(f"Input move: {move}")
        moves = (Move(move.direction, 1) for _ in range(move.amount))
        for move in moves:
            self._move(move)


def parse_input(filename: str) -> Iterator[Move]:
    try:
        f = open(filename)
    except OSError as err:
        print(f"Couldn't open file {filename}. Error: {err}")
    else:
        direction_map = {
            "L": Direction.LEFT,
            "R": Direction.RIGHT,
            "U": Direction.UP,
            "D": Direction.DOWN,
        }
        with f:
            for line in f:
                direction, number = line.strip().split()
                yield Move(direction=direction_map[direction], amount=int(number))


def part_1(input_: list[Move]):
    rope = Rope(2)
    for i in input_:
        rope.move(i)
    print(len(rope.moves))


def part_2(input_: list[Move]):
    rope = Rope(10)
    for i in input_:
        rope.move(i)
    print(len(rope.moves))


def main() -> None:
    input_ = list(parse_input("input"))
    part_1(input_)
    part_2(input_)



if __name__ == "__main__":
    main()
