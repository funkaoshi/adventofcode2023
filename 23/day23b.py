import argparse
import functools
import sys
from dataclasses import dataclass

sys.setrecursionlimit(5000)


@dataclass(frozen=True)
class Point:
    j: int
    i: int


def parse_file(file):
    return tuple([tuple([c for c in line]) for line in file])


def get_neighbours(point: Point, garden_map: tuple[tuple[str]]):
    i = point.i
    j = point.j

    assert garden_map[j][i] != "#"

    left = Point(j, i - 1)
    right = Point(j, i + 1)
    up = Point(j - 1, i)
    down = Point(j + 1, i)

    can_move_right = i < len(garden_map) - 1 and garden_map[j][i + 1] != "#"
    can_move_left = i > 0 and garden_map[j][i - 1] != "#"
    can_move_up = j > 0 and garden_map[j - 1][i] != "#"
    can_move_down = j < len(garden_map[0]) - 1 and garden_map[j + 1][i] != "#"

    neighbours = []

    if can_move_right:
        neighbours.append(right)
    if can_move_left:
        neighbours.append(left)
    if can_move_up:
        neighbours.append(up)
    if can_move_down:
        neighbours.append(down)

    return neighbours


def longest_walk(
    start: Point, end: Point, garden_map: tuple[tuple[str]]
) -> dict[Point, int]:
    """Returns true if we have a path from start to end, false otherwise."""
    distances: dict[Point, int] = {}
    current = [start]
    distance = 1
    while True:
        neighbours = [
            neighbours for n in current for neighbours in get_neighbours(n, garden_map)
        ]

        print(f"{distance}: {neighbours}")

        next_nodes: list[Point] = []
        for node in neighbours:
            if node not in distances:
                distances[node] = distance
                next_nodes.append(node)

        if not next_nodes:
            break

        current = next_nodes

        distance += 1

    return distances


@functools.cache
def longest_walk_recurse(
    start: Point, end: Point, visited: tuple[Point, ...], garden_map: tuple[tuple[str]]
) -> tuple[Point, ...]:
    if start == end:
        print(f"{len(visited)} steps: {visited[0:2]} ... {visited[-2:]}")
        return (start,)

    paths = []
    for neighbour in get_neighbours(start, garden_map):
        if neighbour in visited:
            continue
        path = longest_walk_recurse(neighbour, end, visited + (start,), garden_map)
        if path:
            paths.append((start,) + path)

    if not paths:
        return tuple()

    return max(paths, key=len)


def find_true_start(start, garden_map):
    visited = [start]
    while True:
        neighbours = [
            n for n in get_neighbours(visited[-1], garden_map) if n not in visited
        ]

        if len(neighbours) > 1:
            # we have an actual branch!
            return visited

        visited.append(neighbours[0])


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

    start = Point(0, "".join(garden_map[0]).find("."))
    end = Point(len(garden_map) - 1, "".join(garden_map[-1]).find("."))

    print(f"{start} -> {end}")

    start = find_true_start(start, garden_map)[-1]
    end = find_true_start(end, garden_map)[-1]

    print(f"True {start} -> {end}")

    path = longest_walk_recurse(end, start, tuple(), garden_map)

    print(len(path))
