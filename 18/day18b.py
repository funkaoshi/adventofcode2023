import argparse
from dataclasses import dataclass


@dataclass
class Instruction:
    direction: str
    length: int
    colour: str


@dataclass
class Point:
    x: int
    y: int


Plans = list[Instruction]


def parse_plans(filename: str) -> Plans:
    instructions: Plans = []
    with open(filename) as f:
        lines = f.read().splitlines()
    for line in lines:
        direction, length, colour = line.split(" ")
        instructions.append(Instruction(direction, int(length), colour))
    return instructions


def convert_plans(instructions: Plans) -> Plans:
    new_plans = []
    for i in instructions:
        colour = i.colour[2:-1]  # just keep digits
        distance = int(colour[0:5], 16)

        if colour[-1] == "0":
            direction = "R"
        elif colour[-1] == "1":
            direction = "D"
        elif colour[-1] == "2":
            direction = "L"
        elif colour[-1] == "3":
            direction = "U"
        else:
            raise ValueError(f"Invalid Direction {colour[-1]}")

        # print(f"{colour} -> {direction} {distance}")

        new_plans.append(Instruction(direction, distance, i.colour))
    return new_plans


def draw_trench(instructions: Plans) -> list[tuple[int, int]]:
    polygon = [(0, 0)]
    for i in instructions:
        polygon.append(move(*polygon[-1], i))
    return polygon


def move(x: int, y: int, instruction: Instruction) -> tuple[int, int]:
    direction, length = instruction.direction, instruction.length
    if direction == "U":
        y -= length
    elif direction == "D":
        y += length
    elif direction == "R":
        x += length
    elif direction == "L":
        x -= length
    else:
        raise ValueError(f"Invalid Direction {direction}")
    return (x, y)


def shoelace_algorithm(points: list[tuple[int, int]]) -> int:
    assert points[0] == points[-1]

    total = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        total += x1 * y2 - x2 * y1

    return abs(total) // 2


def manhattan_distance(points: list[tuple[int, int]]) -> int:
    assert points[0] == points[-1]

    total = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        total += abs(x1 - x2) + abs(y1 - y2)

    return total


def picks_theorem(interior_area: int, boundary_points: int) -> float:
    return interior_area + boundary_points / 2 + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="test.txt")
    args = parser.parse_args()

    filename = args.filename

    instructions = parse_plans(filename)
    polygon = draw_trench(instructions)
    interior_area = shoelace_algorithm(polygon)
    border = manhattan_distance(polygon)
    area = picks_theorem(interior_area, border)
    print(f"Problem 1 Area: {area}")

    instructions = parse_plans(filename)
    new_plans = convert_plans(instructions)
    polygon = draw_trench(new_plans)
    interior_area = shoelace_algorithm(polygon)
    border = manhattan_distance(polygon)
    area = picks_theorem(interior_area, border)
    print(f"Problem 2 Area: {area}")
