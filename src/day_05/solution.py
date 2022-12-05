import re
from collections import defaultdict, namedtuple

Job = namedtuple("Job", ["start", "target", "amount"])


class CratePlant:
    def __init__(self) -> None:
        self.stacks: dict[int, list[str]] = {}
        self.jobs: list[Job] = []

    def create_stack(self, *crates: str, positon: int) -> None:
        self.stacks[positon] = list(crates)

    def add_job(self, job: Job) -> None:
        self.jobs.append(job)

    def move_crates(self, job: Job) -> None:
        for _ in range(job.amount):
            last_crate = self.stacks[job.start].pop()
            self.stacks[job.target].append(last_crate)

    def perform_jobs(self) -> None:
        for job in self.jobs:
            self.move_crates(job)

    def get_top_crates(self) -> str:
        return "".join(crates[-1] for _, crates in sorted(self.stacks.items()))

    def __str__(self) -> str:
        d = dict(sorted(self.stacks.items()))
        return "\n".join(f"{k}: {v}" for k, v in d.items())


class CratePlantv2(CratePlant):
    def move_crates(self, job: Job) -> None:
        _stack = []
        for _ in range(job.amount):
            _stack.append(self.stacks[job.start].pop())
        self.stacks[job.target].extend(reversed(_stack))


def parse_input(filename: str, plant: CratePlant) -> None:
    try:
        f = open(filename)
    except OSError as err:
        print(f"Couldn't open file {filename}. Error: {err}")
    else:
        with f:
            regex = re.compile(r"( {3}|\[\S\]) ?")
            stacks = defaultdict(list)
            while (line := next(f)) != "\n":
                if m := regex.findall(line):
                    for idx, i in enumerate(m, start=1):
                        if i.strip():
                            i = i.strip("[]")
                            stacks[idx].append(i)

            for positon, crates in stacks.items():
                plant.create_stack(*reversed(crates), positon=positon)

            regex = re.compile(
                r"move (?P<amount>\d+) from (?P<start>\d+) to (?P<target>\d+)"
            )
            for line in f:
                if k := regex.match(line):
                    plant.add_job(
                        Job(
                            int(k.group("start")),
                            int(k.group("target")),
                            int(k.group("amount")),
                        )
                    )


def main() -> None:
    crate_plant = CratePlant()
    parse_input("input_example", crate_plant)
    crate_plant.perform_jobs()
    print(crate_plant.get_top_crates())

    crate_plant = CratePlant()
    parse_input("input", crate_plant)
    crate_plant.perform_jobs()
    print(crate_plant.get_top_crates())

    crate_plant = CratePlantv2()
    parse_input("input_example", crate_plant)
    crate_plant.perform_jobs()
    print(crate_plant.get_top_crates())

    crate_plant = CratePlantv2()
    parse_input("input", crate_plant)
    crate_plant.perform_jobs()
    print(crate_plant.get_top_crates())


if __name__ == "__main__":
    main()
