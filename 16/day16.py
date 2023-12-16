import argparse
import enum
from dataclasses import dataclass


class Direction(enum.Enum):
    right = 0
    left = 1
    up = 2
    down = 3


@dataclass
class Vector:
    x: int
    y: int
    direction: Direction


def get_next_tiles(vector: Vector, cave: list[list[str]]) -> list[Vector]:
    current_tile = cave[vector.y][vector.x]
    next_tiles = []

    if vector.direction == Direction.right:
        if current_tile in [".", "-"] and vector.x + 1 < len(cave[vector.y]):
            # continue moving right
            next_tiles.append(Vector(vector.x + 1, vector.y, vector.direction))

        if current_tile in ["/", "|"] and vector.y - 1 >= 0:
            # reflect up
            next_tiles.append(Vector(vector.x, vector.y - 1, Direction.up))

        if current_tile in ["\\", "|"] and vector.y + 1 < len(cave):
            # reflect down
            next_tiles.append(Vector(vector.x, vector.y + 1, Direction.down))

    elif vector.direction == Direction.left:
        if current_tile in [".", "-"] and vector.x - 1 >= 0:
            # continue moving left
            next_tiles.append(Vector(vector.x - 1, vector.y, vector.direction))

        if current_tile in ["/", "|"] and vector.y + 1 < len(cave):
            # reflect down
            next_tiles.append(Vector(vector.x, vector.y + 1, Direction.down))

        if current_tile in ["\\", "|"] and vector.y - 1 >= 0:
            # reflect up
            next_tiles.append(Vector(vector.x, vector.y - 1, Direction.up))

    elif vector.direction == Direction.up:
        if current_tile in [".", "|"] and vector.y - 1 >= 0:
            # continue moving up
            next_tiles.append(Vector(vector.x, vector.y - 1, vector.direction))

        if current_tile in ["/", "-"] and vector.x + 1 < len(cave[vector.y]):
            # reflect right
            next_tiles.append(Vector(vector.x + 1, vector.y, Direction.right))

        if current_tile in ["\\", "-"] and vector.x - 1 >= 0:
            # reflect left
            next_tiles.append(Vector(vector.x - 1, vector.y, Direction.left))

    elif vector.direction == Direction.down:
        if current_tile in [".", "|"] and vector.y + 1 < len(cave):
            # continue moving down
            next_tiles.append(Vector(vector.x, vector.y + 1, vector.direction))

        if current_tile in ["/", "-"] and vector.x - 1 >= 0:
            # reflect left
            next_tiles.append(Vector(vector.x - 1, vector.y, Direction.left))

        if current_tile in ["\\", "-"] and vector.x + 1 < len(cave[vector.y]):
            # reflect right
            next_tiles.append(Vector(vector.x + 1, vector.y, Direction.right))

    else:
        raise ValueError(f"Unknown direction {vector.direction}")

    if len(next_tiles) > 2:
        raise ValueError(f"Incorrectly calculated next tiles for {vector}")

    return next_tiles


def get_energized(cave: list[list[str]], start: list[Vector]) -> int:
    already_travelled = set()
    energized = set()
    while True:
        new_start = []
        for vector in start:
            # every tile light is passing through is energized
            energized.add((vector.y, vector.x))

            # if we've already travelled this path we don't need to do it again
            if (vector.x, vector.y, vector.direction) not in already_travelled:
                already_travelled.add((vector.x, vector.y, vector.direction))
                new_start += get_next_tiles(vector, cave)

        if not new_start:
            break

        start = new_start

    return len(energized)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="test.txt")
    args = parser.parse_args()

    filename = args.filename

    with open(filename) as f:
        cave = [list(line) for line in f.read().splitlines()]

    start = [Vector(0, 0, Direction.right)]

    print(f"Problem 1: {get_energized(cave, start)}")

    max_energized = 0
    for x in range(len(cave[0])):
        energized = get_energized(cave, [Vector(x, 0, Direction.down)])
        if energized > max_energized:
            max_energized = energized

        energized = get_energized(cave, [Vector(x, len(cave) - 1, Direction.up)])
        if energized > max_energized:
            max_energized = energized

    for y in range(len(cave)):
        energized = get_energized(cave, [Vector(0, y, Direction.right)])
        if energized > max_energized:
            max_energized = energized

        energized = get_energized(cave, [Vector(len(cave[0]) - 1, y, Direction.left)])
        if energized > max_energized:
            max_energized = energized

    print(f"Problem 2: {max_energized}")
