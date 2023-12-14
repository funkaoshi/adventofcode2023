import argparse
import re

rock_re = re.compile(r"([O.]+)|(#+)")


def tilt(rocks):
    tilted_rocks = []
    for row in rocks:
        s = ""
        for r in rock_re.finditer(row):
            r = r.group()
            count = r.count("O")
            if count:
                r = "O" * count + "." * (len(r) - count)
            s += r
        tilted_rocks.append(s)
    return tilted_rocks


def rotate_rocks(rocks):
    rotated_rocks = []
    for i in range(len(rocks[0])):
        col = [rocks[j][i] for j in range(len(rocks))]
        rotated_rocks.append("".join(col))
    return rotated_rocks


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="input.txt")
    args = parser.parse_args()

    filename = args.filename

    with open(filename) as f:
        rocks = f.read().splitlines()

    # we rotate the input so we can work on rows rather than columns
    rocks = rotate_rocks(rocks)

    # "tilt" the platform so the rocks move "north"
    rocks = tilt(rocks)

    # load is the distance from the bottom of the platform, or in our case the
    # start of the string, so we can simply note the location of the rock and
    # subtrack that from the length of the string.
    max_load = len(rocks)
    total_load = sum(
        [max_load - i for row in rocks for i, c in enumerate(row) if c == "O"]
    )

    print(total_load)
