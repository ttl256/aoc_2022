from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator

class Instruction(Enum):
    ADDX = auto()
    NOOP = auto()

@dataclass
class Entry:
    instruction: Instruction
    value: int

class Circuit:
    def __init__(self, entries: list[Entry]):
        self.entries = entries
        self.cycle = 0
        self.register = 1

    def tick(self):
        self.cycle += 1

    def __iter__(self):
        cycles_to_exec = {
            Instruction.ADDX: 2,
            Instruction.NOOP: 1,
        }
        for entry in self.entries:
            for cycle in range(cycles_to_exec[entry.instruction]):
                self.tick()
                yield self.cycle, self.register, entry
                if cycle == len(range(cycles_to_exec[entry.instruction])) - 1:
                    self.register += entry.value


def parse_instruction(line: str) -> Entry:
    args = line.strip().split()
    if args[0] == "noop":
        return Entry(Instruction.NOOP, 0)
    elif args[0] == "addx":
        return Entry(Instruction.ADDX, int(args[1]))
    else:
        raise AssertionError(f"Unknown instruction: {args}")

def parse_input(filename: str) -> Iterator[Entry]:
    try:
        f = open(filename)
    except OSError as err:
        print(f"Couldn't open file {filename}. Error: {err}")
    else:
        with f:
            for line in f:
                yield parse_instruction(line)

def part_1() -> int:
    circuit = Circuit(list(parse_input("input")))
    interesting_cycles = range(20, 221, 40)
    all_signal_strenghts = 0
    for cycle, register, entry in circuit:
        if cycle in interesting_cycles:
            signal_strenght = cycle * register
            all_signal_strenghts += signal_strenght
    return all_signal_strenghts

def part_2() -> str:
    circuit = Circuit(list(parse_input("input")))
    all_lines = []
    line = []
    for cycle, register, entry in circuit:
        sprite = range(register - 1, register + 2)
        cycle = (cycle - 1) % 40
        if cycle in sprite:
            line.append("#")
        else:
            line.append(".")
        if len(line) == 40:
            all_lines.append("".join(line))
            line.clear()
    return "\n".join(all_lines)

def main() -> None:
    print(part_1())
    print(part_2())



if __name__ == "__main__":
    main()
