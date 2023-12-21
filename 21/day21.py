import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    i: int
    j: int


def parse_file(file):
    return [[c for c in line] for line in file]


def get_neighbors(point: Point, garden_map: list[list[str]]):
    neighbors = []

    if point.i > 0 and garden_map[point.j][point.i - 1] != "#":
        neighbors.append(Point(point.i - 1, point.j))
    if point.i < len(garden_map) - 1 and garden_map[point.j][point.i + 1] != "#":
        neighbors.append(Point(point.i + 1, point.j))
    if point.j > 0 and garden_map[point.j - 1][point.i] != "#":
        neighbors.append(Point(point.i, point.j - 1))
    if point.j < len(garden_map[0]) - 1 and garden_map[point.j + 1][point.i] != "#":
        neighbors.append(Point(point.i, point.j + 1))

    return neighbors


def walk_garden_map(start: set[Point], garden_map: list[list[str]]) -> set[Point]:
    neighbors = set()
    for point in start:
        neighbors.update(get_neighbors(point, garden_map))
    return neighbors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="test.txt")
    parser.add_argument("-c", "--count", action="store", default=1)
    args = parser.parse_args()

    filename = args.filename
    count = int(args.count)

    with open(filename) as f:
        file = f.read().splitlines()

    garden_map = parse_file(file)

    for j in range(len(garden_map)):
        for i in range(len(garden_map[j])):
            if garden_map[j][i] == "S":
                s = Point(i, j)
                break

    visited = set([s])
    for _ in range(count):
        visited = walk_garden_map(visited, garden_map)

    print(len(set(visited)))
