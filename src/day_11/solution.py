from collections import deque
from operator import add, mul, pow
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Iterable, Iterator
from itertools import takewhile
from functools import partial, reduce


class Monkey:
    def __init__(
        self,
        *items: int,
        id_: int,
        test_value: int,
        test_true: int,
        test_false: int,
        operation,
        operation_value: int,
    ):
        self.id_: int = id_
        self.items: deque[int] = deque(items)
        self.test_value: int = test_value
        self.test_true: int = test_true
        self.test_false: int = test_false
        self.operation = operation
        self.operation_value = operation_value
        self.inspections = 0

    def make_operation(self, item) -> int:
        if self.operation_value is None:
            # print("!!! SQRT !!!")
            return int(self.operation(item))
        return int(self.operation(item, self.operation_value))

    def inspect(self, item: int):
        self.inspections += 1
        return self.make_operation(item)

    def decrease_worry_level(self, item: int):
        return int(item // 3)

    def test_item(self, item: int):
        if item % self.test_value == 0:
            return self.test_true
        else:
            return self.test_false

    def __str__(self):
        # attrs = (
        #     "id_",
        #     "test_value",
        #     "test_true",
        #     "test_false",
        #     "operation",
        #     "operation_value",
        #     "items",
        # )
        # return "\n".join(repr(getattr(self, i)) for i in attrs)
        return f"Monkey {self.id_}: {','.join(map(str, self.items))}"

class MonkeyParty(dict[int, Monkey]):
    def __init__(self, *monkeys: Monkey):
        for monkey in monkeys:
            self[monkey.id_] = monkey

    def play_turn(self, id_:int):
        monkey = self[id_]
        # print(f"Turn for: {monkey}")
        # print(f"{monkey.operation=}, {monkey.operation_value}")
        while monkey.items:
            # print(monkey)
            item = monkey.items.popleft()
            # print(f"Current item: {item}")
            item = monkey.inspect(item)
            # print(f"Item after inspection: {item}")
            # item = monkey.decrease_worry_level(item)
            # print(f"Item after decreasing worry level: {item}")
            id_to_throw = monkey.test_item(item)
            # print(f"Id to throw: {id_to_throw}")
            self[id_to_throw].items.append(item)
            # print(f"Monkey with the new item: {self[id_to_throw]}")

    def play_round(self):
        for monkey in self:
            self.play_turn(monkey)


def parse_input(filename: str) -> Iterator[list[str]]:
    try:
        f = open(filename)
    except OSError as err:
        print(f"Couldn't open file {filename}. Error: {err}")
    else:
        with f:
            while True:
                block = takewhile(lambda s: s != "\n", f)
                block = list(line.strip() for line in block)
                if not block:
                    return
                yield block


def create_monkey(description: Iterable[str]) -> Monkey:
    monkey = {}
    for line in description:
        if "Monkey" in line:
            _, id_ = line.strip(":").split()
            monkey["id_"] = int(id_)
        elif "Starting items" in line:
            line = line.strip().lstrip("Starting items: ")
            items = map(int, line.split(", "))
            # monkey["items"] = items
        elif "Operation" in line:
            line = line.strip().lstrip("Operation: new = old ")
            if "* old" in line:
                monkey["operation"] = partial(lambda x, y: pow(x, y), y=2)
                monkey["operation_value"] = None
            else:
                op, val = line.split()
                if op == "+":
                    monkey["operation"] = add
                if op == "*":
                    monkey["operation"] = mul
                monkey["operation_value"] = int(val)
        elif "Test:" in line:
            line = line.strip().lstrip("Test: divisible by ")
            monkey["test_value"] = int(line)
        elif "If true: " in line:
            line = line.strip().lstrip("If true: throw to monkey ")
            monkey["test_true"] = int(line)
        elif "If false: " in line:
            line = line.strip().lstrip("If false: throw to monkey ")
            monkey["test_false"] = int(line)
    return Monkey(*items, **monkey)


def part_1() -> int:
    ...


def part_2() -> str:
    ...


def main() -> None:
    # sys.set_int_max_str_digits(1000000)
    monkeys = [create_monkey(block) for block in parse_input("input")]
    party = MonkeyParty(*monkeys)
    for i in range(10000):
        print(f"Round: {i}")
        party.play_round()
    for id_, monkey in party.items():
        print(monkey)
    print(reduce(mul, sorted((monkey.inspections for id, monkey in party.items()), reverse=True)[:2], 1))

    print(part_1())
    print(part_2())


if __name__ == "__main__":
    main()
