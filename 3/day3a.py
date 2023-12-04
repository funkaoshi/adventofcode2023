
# Read the "engine schematic" and replace new lines with "." to simplify processing
with open("input.txt") as f:
    engine = [l.replace("\n", ".") for l in f.readlines()]

# the list of valid parts we have found
parts = []

# state variables to track the current part we are reading and if it is valid
current_part = ""
valid_part = False

for y in range(len(engine)):
    for x in range(len(engine[y])):

        # Process a new DIGIT
        if engine[y][x] in "0123456789":
            if not current_part and not valid_part:
                # started reading a possible new part, check proceeding diagonals
                sw = (
                    x - 1 >= 0
                    and y - 1 >= 0
                    and engine[y - 1][x - 1] not in ".0123456789"
                )
                nw = (
                    x - 1 >= 0
                    and y < len(engine) - 1
                    and engine[y + 1][x - 1] not in ".0123456789"
                )
                valid_part = nw or sw

            # read a digit so include it in our current part tracker
            current_part += engine[y][x]

        if current_part and not valid_part:
            # check area around the part we are reading. We need to worry about
            # the area above and below this line.
            below = y - 1 >= 0 and engine[y - 1][x] not in ".0123456789"
            above = y < len(engine) - 1 and engine[y + 1][x] not in ".0123456789"
            valid_part = above or below

        # Process a PERIOD
        if engine[y][x] == ".":
            if current_part and valid_part:
                # if we have read a part and it's adjacent to a symbol we store it
                parts.append(current_part)

            # reset the valid part and current part values
            current_part = ""
            valid_part = False

        # Process a SYMBOL
        if engine[y][x] not in ".0123456789":  # we have read a symbol
            if current_part:
                # save the part we have finished reading
                parts.append(current_part)

                # this symbol demarcates the end of the part string
                current_part = ""

            # this could be a valid for the next part
            valid_part = True


print(sum([int(part) for part in parts]))
