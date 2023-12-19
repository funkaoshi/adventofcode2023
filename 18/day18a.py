import argparse
from dataclasses import dataclass


@dataclass
class Instruction:
    direction: str
    length: int
    colour: str


Plans = list[Instruction]


colour_map: dict[tuple[int, int], str] = {}


def parse_plans(filename: str) -> Plans:
    instructions: Plans = []
    with open(filename) as f:
        lines = f.read().splitlines()
    for line in lines:
        direction, length, colour = line.split(" ")
        instructions.append(Instruction(direction, int(length), colour))
    return instructions


def dig_trench(instructions: Plans) -> list[str]:
    trench = [["." for i in range(1000)] for _ in range(1000)]
    x = len(trench[0]) // 2
    y = len(trench) // 2

    for count, i in enumerate(instructions):
        new_x, new_y = move(x, y, i)

        print(f"Moving {i.direction} {i.length}: from {x},{y} to {new_x},{new_y}")

        start_x, end_x = min(x, new_x), max(x, new_x)
        start_y, end_y = min(y, new_y), max(y, new_y)

        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                trench[y][x] = "#"
                colour_map[(y, x)] = i.colour

        x, y = new_x, new_y

    filled_trench = flood_fill(trench, len(trench[0]) // 2 + 1, len(trench) // 2 + 1)

    return filled_trench


def flood_fill(trench: list[list[str]], x: int, y: int) -> list[str]:
    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        if trench[y][x] == "#":
            continue
        trench[y][x] = "#"
        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

    return ["".join(line) for line in trench]


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


def calculate_volume(trench: list[str]) -> int:
    volume = 0
    for row in trench:
        volume += row.count("#")
    return volume


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="test.txt")
    args = parser.parse_args()

    filename = args.filename

    instructions = parse_plans(filename)
    trench = dig_trench(instructions)
    volume = calculate_volume(trench)

    print(volume)
