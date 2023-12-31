import sys
from typing import List


def check_adjacent_symbols(engine: List[str], x: int, y: int) -> bool:
    # look for gears around the current position
    above = y - 1 >= 0 and engine[y - 1][x] not in ".0123456789"
    below = y + 1 < len(engine) and engine[y + 1][x] not in ".0123456789"
    current = engine[y][x] not in ".0123456789"

    return above or below or current


filename = "input.txt" if not len(sys.argv) > 1 else sys.argv[1]

with open(filename) as f:
    engine = [line.replace("\n", ".") for line in f.readlines()]

# the list of valid parts we have found
parts = []

# the current possible part number we are reading
current_part = ""

# tracks wether the part we are currently reading is adjacent to a symbol
valid_part = False

for y in range(len(engine)):
    for x in range(len(engine[y])):
        try:
            next_char_is_digit = engine[y][x + 1] in "0123456789"
        except IndexError:
            next_char_is_digit = False

        if engine[y][x] in "0123456789":
            current_part += engine[y][x]

        if current_part or next_char_is_digit:
            # As we read a part number we will check for adjacent symbols
            # in the rectangle around it.
            valid_part = valid_part or check_adjacent_symbols(engine, x, y)

        if engine[y][x] not in "0123456789":
            # read a period or symbol (., *, etc). Every line ends with a '.'
            # so we willalways reset the current_part / valid_part state variables.

            if current_part and valid_part:
                parts.append(current_part)

            # reset the valid part and current part values
            current_part = ""

            if next_char_is_digit:
                # reset to just the symbols adjacent to the next part
                # TODO: called twice when starting a new part
                valid_part = check_adjacent_symbols(engine, x, y)
            else:
                valid_part = False

total_parts = sum([int(part) for part in parts])

print(f"Total parts {total_parts}.")
