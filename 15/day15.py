import argparse
import collections
import dataclasses
import re


@dataclasses.dataclass
class Lens:
    label: str
    focal_length: int


# example commands: rn=1, cm-, qp=3
command_re = re.compile(r"^([a-zA-Z]+)(=|-)(\d+)?$")


def hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def hashmap(commands: list[str]) -> dict[int, list[Lens]]:
    boxes: dict[int, list[Lens]] = collections.defaultdict(list)
    for command in commands:
        if match := command_re.match(command):
            label, operation, focal_length = match.groups()
        else:
            # invalid command
            raise Exception

        box_id = hash(label)
        if operation == "-":
            for i, lens in enumerate(boxes[box_id]):
                if lens.label == label:
                    del boxes[box_id][i]
                    break
        elif operation == "=":
            for i, lens in enumerate(boxes[box_id]):
                if lens.label == label:
                    boxes[box_id][i].focal_length = int(focal_length)
                    break
            else:
                boxes[box_id].append(Lens(label, int(focal_length)))
        else:
            print("Invalid command {command}.")
            raise Exception

        # print(f"After '{command}':")
        # for i, box in boxes.items():
        #     print(f"Box {i}: {[l + ' ' + str(f) for l, f in box]}")

    return boxes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="test.txt")
    args = parser.parse_args()

    filename = args.filename

    with open(filename) as f:
        commands = f.read().strip().split(",")

    hashes = [hash(command) for command in commands]
    print(f"Problem 1: {sum(hashes)}")

    boxes = hashmap(commands)
    focal_lengths = [
        (i + 1) * j * lens.focal_length
        for i, box in boxes.items()
        for j, lens in enumerate(box, start=1)
    ]
    print(f"Problem 2: {sum(focal_lengths)}")
