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


def find_first_branch(start, garden_map) -> list[Point]:
    visited = [start]
    while True:
        neighbours = [
            n for n in get_neighbours(visited[-1], garden_map) if n not in visited
        ]

        if len(neighbours) > 1:
            # we have an actual branch!
            return visited

        if not neighbours:
            return visited[:-1]

        visited.append(neighbours[0])


def get_neighbours(point: Point, garden_map: tuple[tuple[str]]):
    i = point.i
    j = point.j

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
        if garden_map[j][i] == ">":
            return [right]
        else:
            neighbours.append(right)
    if can_move_left:
        if garden_map[j][i] == "<":
            return [left]
        else:
            neighbours.append(left)
    if can_move_up:
        if garden_map[j][i] == "^":
            return [up]
        else:
            neighbours.append(up)
    if can_move_down:
        if garden_map[j][i] == "v":
            return [down]
        else:
            neighbours.append(down)

    return neighbours


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

    true_start = find_first_branch(start, garden_map)
    true_end = find_first_branch(end, garden_map)

    path = longest_walk_recurse(true_start[-1], true_end[-1], tuple(), garden_map)

    print(len(true_start) + len(path) + len(true_end) - 2)
