import argparse
import collections
import re

# example commands: rn=1, cm-, qp=3
command_re = re.compile(r"^([a-zA-Z]+)(=|-)(\d+)?$")


def hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def hashmap(commands: list[str]) -> dict[int, dict[str, int]]:
    boxes: dict[int, dict[str, int]] = collections.defaultdict(collections.OrderedDict)
    for command in commands:
        if match := command_re.match(command):
            label, operation, focal_length = match.groups()
        else:
            # invalid command
            raise Exception

        box_id = hash(label)
        if operation == "-":
            # remove lens from appropriate box (if it exists)
            if label in boxes[box_id]:
                del boxes[box_id][label]
        elif operation == "=":
            # add the lens to the appropriate box, replacing (in-place) if
            # there is already a lens with the same label within the box
            boxes[box_id][label] = int(focal_length)
        else:
            print("Invalid command {command}.")
            raise Exception

        # print(f"After '{command}':")
        # for i, box in boxes.items():
        #     print(f"Box {i}: {[l + ' ' + str(f) for l, f in box.items()]}")

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
        (i + 1) * j * focal_length
        for i, box in boxes.items()
        for j, (label, focal_length) in enumerate(box.items(), start=1)
    ]
    print(f"Problem 2: {sum(focal_lengths)}")
