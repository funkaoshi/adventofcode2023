from collections import defaultdict
from typing import List, Tuple
import sys


def get_adjacent_gears(engine, x, y):
    # look for gears around the current position
    valid_gears = []

    above = y - 1 >= 0 and engine[y - 1][x] == "*"
    if above:
        valid_gears.append((y - 1, x))
    
    below = y + 1 < len(engine) and engine[y + 1][x] == "*"
    if below:
        valid_gears.append((y + 1, x))
    
    current = engine[y][x] == "*"
    if current:
        valid_gears.append((y, x))

    return valid_gears


filename = "input.txt" if not len(sys.argv) > 1 else sys.argv[1]

with open(filename) as f:
    engine = [l.replace("\n", ".") for l in f.readlines()]

# list of gears we have found, and the parts adjacent to them
gears = defaultdict(list)

# list of gears we have encountered while reading a part
valid_gears: List[Tuple] = []

# the part we are currently reading
current_part = ""

for y in range(len(engine)):
    for x in range(len(engine[y])):
        try:
            next_char_is_digit = engine[y][x + 1] in "0123456789"
        except IndexError:
            next_char_is_digit = False

        if engine[y][x] in "0123456789":
            current_part += engine[y][x]

        if current_part or next_char_is_digit:
            # Look for any gears in the rectangle that surrounds a gear part.
            valid_gears.extend(get_adjacent_gears(engine, x, y))

        if engine[y][x] not in "0123456789":
            # read a period or symbol (., *, etc). Every line ends with a '.' so we will 
            # always reset the current_part / valid_gears state variables by the time
            # we are done processing the line.

            if current_part:
                print(f"{y} {x} - current_part: {current_part} - valid_gears: {valid_gears}")

            if current_part and valid_gears:
                # save the part next to any adjacent gears
                for gear in valid_gears:
                    gears[gear].append(current_part)

            # terminate the current part
            current_part = ""

            if next_char_is_digit:
                # reset gear list for upcoming part
                # TODO: called twice when starting a new part
                valid_gears = get_adjacent_gears(engine, x, y)
            else:
                valid_gears = []

good_gear_ratios = [
    int(parts[0]) * int(parts[1]) for gear, parts in gears.items() if len(parts) == 2
]
total_gear_ratios = sum(good_gear_ratios)

print(f"Total gear ratios: {total_gear_ratios}")
