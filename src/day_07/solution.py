from collections import defaultdict
import json


def tree_factory():
    return defaultdict(tree_factory)


def populate_dirs(d, *keys):
    for i in keys:
        d = d[i]


def get_nested_value(d, *keys):
    for i in keys:
        d = d[i]
    return d


def insert_files(d, filename, size, *keys):
    for i in keys:
        d = d[i]
    d[filename] = size


def parse_input(filename: str) -> defaultdict:
    """
    Parse input into JSON
    """
    try:
        f = open(filename)
    except OSError as err:
        print(f"Couldn't open file {filename}. Error: {err}")
        return defaultdict()
    else:
        with f:
            tree = tree_factory()
            absolute_path: list[str] = []
            for line in f:
                line = line.strip()
                if line.startswith("$"):
                    line = line.removeprefix("$ ")
                    if "cd" in line:
                        _, dir = line.split()
                        if dir == "..":
                            absolute_path.pop()
                        else:
                            absolute_path.append(dir)
                            populate_dirs(tree, *absolute_path)
                else:
                    size_, filename_ = line.split()
                    try:
                        size = int(size_)
                    except ValueError:
                        continue
                    else:
                        insert_files(tree, filename_, size, *absolute_path)

        return tree


def find_dir_size(tree):
    stack: list[list[str]] = []
    dir_sizes = defaultdict(int)
    for k in tree:
        stack.append([k])
    while stack:
        abs_path = stack.pop()
        val = get_nested_value(tree, *abs_path)
        for k, v in val.items():
            if isinstance(v, dict):
                stack.append(abs_path + [k])
            if isinstance(v, int):
                s = "/"
                dir_sizes[s] += v
                for i in abs_path[1:]:
                    s = f"{s}{i}/"
                    dir_sizes[s] += v
    return dir_sizes


def part_1(tree):
    return sum(v for _, v in find_dir_size(tree).items() if v <= 100000)


def part_2(tree):
    available_space = 70000000
    required_space = 30000000
    dir_sizes = find_dir_size(tree)
    used_space = dir_sizes["/"]
    unused_space = available_space - used_space
    need_to_free = required_space - unused_space
    return sorted(space for _, space in dir_sizes.items() if space > need_to_free)[0]


def main() -> None:
    # tree = parse_input("input_example")
    tree = parse_input("input")
    print(json.dumps(tree, indent=4))
    print(part_1(tree))
    print(part_2(tree))


if __name__ == "__main__":
    main()
