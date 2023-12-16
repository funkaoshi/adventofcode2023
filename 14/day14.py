import argparse
import enum
import functools
import re


class Direction(enum.Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


rock_re = re.compile(r"([O.]+)|(#+)")


@functools.cache
def cycle(rocks: str) -> str:
    for direction in [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]:
        # Perform operations with the direction
        rocks = tilt(rocks, direction)
    return rocks


@functools.cache
def tilt(rocks_str: str, direction: Direction) -> str:
    # We pass around strings rather tha lists so we can cache our results
    rocks = rocks_str.strip().split("\n")

    # transform the rocks array so we are always looking at a row of rocks
    # and shifting rocks to the start of those rows.
    rocks = transform_rocks(rocks, direction)

    tilted_rocks = []
    for row in rocks:
        s = ""
        for match in rock_re.finditer(row):
            r = match.group()
            count = r.count("O")
            if count:
                r = "O" * count + "." * (len(r) - count)
            s += r
        tilted_rocks.append(s)

    # restore the correct orientation of the rocks
    rocks = transform_rocks(tilted_rocks, direction, undo=True)

    return "\n".join(rocks)


def transform_rocks(rocks: list[str], direction: Direction, undo=False):
    if direction == Direction.NORTH:
        return rotate_rocks_north_tilt(rocks)
    elif direction == Direction.SOUTH:
        return rotate_rocks_south_tilt(rocks, undo)
    elif direction == Direction.EAST:
        return flip_rocks_east_tilt(rocks)
    elif direction == Direction.WEST:
        # already correctly oriented for operating on rows
        return rocks

    raise Exception


def rotate_rocks_north_tilt(rocks):
    rotated_rocks = []
    for i in range(len(rocks[0])):
        col = [rocks[j][i] for j in range(len(rocks))]
        rotated_rocks.append("".join(col))
    return rotated_rocks


def rotate_rocks_south_tilt(rocks, undo=False):
    rotated_rocks = []
    if undo:
        for i in range(len(rocks[0]) - 1, -1, -1):
            col = [rocks[j][i] for j in range(len(rocks))]
            rotated_rocks.append("".join(col))
    else:
        for i in range(len(rocks[0])):
            col = [rocks[j][i] for j in range(len(rocks))]
            rotated_rocks.append("".join(reversed(col)))
    return rotated_rocks


def flip_rocks_east_tilt(rocks):
    return ["".join(reversed(row)) for row in rocks]


def calculate_max_load(rocks: list[str]) -> int:
    max_load = len(rocks)
    return sum([max_load - i for row in rocks for i, c in enumerate(row) if c == "O"])


def calculate_max_load_north_tilt(rocks_str: str) -> int:
    # "tilt" the platform so the rocks move "north"
    rocks_str = tilt(rocks_str, Direction.NORTH)

    # load is the distance from the bottom of the platform, or in our case the
    # start of the string, so we can simply note the location of the rock and
    # subtrack that from the length of the string.
    rocks = rotate_rocks_north_tilt(rocks_str.split("\n"))

    return calculate_max_load(rocks)


def calculate_max_load_after_cycles(rocks_str: str, cycles=1000000000) -> int:
    cycle_set = []
    skipped = False
    i = 0
    while i < cycles:
        rocks_str = cycle(rocks_str)

        if not skipped:
            if rocks_str not in cycle_set:
                cycle_set.append(rocks_str)
            else:
                print(f"Found loop after {i} iterations")

                loop_length = i - cycle_set.index(rocks_str) + 1
                loops_in_cycle = cycles % loop_length
                i = cycles - loops_in_cycle
                skipped = True

                print(f"Skip ahead to iteration {i}. {loop_length=} {loops_in_cycle=}")

        i += 1

    # rotate our result after all the cycles so we can calculate the load
    # (along a row rather than column.)
    rocks = rotate_rocks_north_tilt(rocks_str.split("\n"))

    return calculate_max_load(rocks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="input.txt")
    parser.add_argument("-c", "--cycles", action="store", default=1000000000)
    args = parser.parse_args()

    filename = args.filename
    cycles = int(args.cycles)

    with open(filename) as f:
        rocks = f.read()

    print(calculate_max_load_north_tilt(rocks))
    print(calculate_max_load_after_cycles(rocks, cycles))
