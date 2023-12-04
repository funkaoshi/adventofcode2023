from collections import defaultdict
from typing import List, Tuple
import sys

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
        # we can read through the input text file once, looking at each character
        # and some of the characters around each position as needed to find
        # valid gears.

        # Process a new DIGIT
        if engine[y][x] in "0123456789":
            # read a digit so include it in our current part tracker
            current_part += engine[y][x]

        if current_part:
            # look for gears around the part we are reading. We want to track
            # any we find so we can store this part as adjacent to it.

            below = y - 1 >= 0 and engine[y - 1][x] == "*"
            above = y + 1 < len(engine) and engine[y + 1][x] == "*"

            if above:
                valid_gears.append((y + 1, x))
            if below:
                valid_gears.append((y - 1, x))

            if len(current_part) == 1:
                # started reading a possible new part, check proceeding diagonals
                # as well. We don't need to look to the right of the part because we
                # will terminate processing a part number on a '.' or symbol.
                diagonal_below = (
                    x - 1 >= 0 and y - 1 >= 0 and engine[y - 1][x - 1] == "*"
                )
                diagonal_above = (
                    x - 1 >= 0 and y + 1 < len(engine) and engine[y + 1][x - 1] == "*"
                )
                before = x - 1 >= 0 and engine[y][x - 1] == "*"

                if diagonal_below:
                    valid_gears.append((y - 1, x - 1))
                if diagonal_above:
                    valid_gears.append((y + 1, x - 1))
                if before:
                    valid_gears.append((y, x - 1))

        if current_part and engine[y][x] == "*":
            valid_gears.append((y, x))

        if engine[y][x] == "." or engine[y][x] == "*":
            if current_part and valid_gears:
                for gear in valid_gears:
                    gears[gear].append(current_part)

            current_part = ""
            valid_gears = []

good_gear_ratios = [
    int(parts[0]) * int(parts[1]) for gear, parts in gears.items() if len(parts) == 2
]

print(sum(good_gear_ratios))
