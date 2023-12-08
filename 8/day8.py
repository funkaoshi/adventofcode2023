import math
import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Locations:
    left: str
    right: str


def load_instructions_and_coordinates(filename: str) -> dict:
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    # first line is the right/left instruction sequence
    instructions = lines.pop(0)

    # drop blank line
    lines.pop(0)

    coordinate_map_re = re.compile(r"(\w+) = \((\w+), (\w+)\)")

    locations: dict[str, str | Locations] = {}
    while True:
        try:
            if match := coordinate_map_re.match(lines.pop(0)):
                start, left, right = match.group(1), match.group(2), match.group(3)
        except IndexError:
            break

        locations[start] = Locations(left, right)

    locations["instructions"] = instructions

    return locations


def find_routes(start: list[str], locations: dict) -> list[int]:
    instructions: list[str] = []
    steps: list[int] = []
    counter = 0

    while True:
        for s in start:
            if s.endswith("Z"):
                steps.append(counter)

        if not instructions:
            instructions = list(locations["instructions"])

        instruction = instructions.pop(0)

        start = [
            locations[s].left if instruction == "L" else locations[s].right
            for s in start
            if not s.endswith("Z")
        ]

        counter += 1

        if not start:
            break

    return steps


filename = "input.txt" if len(sys.argv) == 1 else sys.argv[1]

locations = load_instructions_and_coordinates(filename)

problem_one_steps = find_routes(["AAA"], locations)
print(f"{math.lcm(*problem_one_steps)}")

start = [key for key in locations.keys() if key.endswith("A")]
problem_two_steps = find_routes(start, locations)
print(f"{math.lcm(*problem_two_steps)}")
