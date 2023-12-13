import argparse


def get_patterns(filename):
    with open(filename) as f:
        file = f.read().splitlines() + [""]

    patterns = []
    current_pattern = []
    while file:
        line = file.pop(0)
        if line:
            current_pattern.append(list(line))
        else:
            patterns.append(current_pattern)
            current_pattern = []

    return patterns


def print_pattern(pattern):
    for line in pattern:
        print(line)
    print()


def find_horizontal_reflection_index(pattern):
    if len(pattern) % 2 == 1:
        # an odd number of rows can't be reflected
        return None

    if len(pattern) == 0:
        # an empty pattern can't be reflected
        return None

    mid_point = len(pattern) // 2

    first_half = pattern[0:mid_point]
    second_half = list(reversed(pattern[mid_point:]))

    # if the two halves are the same, we have found the mirror's location
    return mid_point if first_half == second_half else None


def rotate(pattern):
    # pivot the pattern 90 degrees
    return [
        [pattern[j][i] for j in range(len(pattern))] for i in range(len(pattern[0]))
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="input.txt")
    args = parser.parse_args()

    filename = args.filename

    reflection_point_score = 0
    reflection_point = None
    patterns = get_patterns(filename)

    for pattern in patterns:
        for i in range(len(pattern)):
            reflection_point = find_horizontal_reflection_index(pattern[i:])
            if reflection_point is not None:
                reflection_point += i
                reflection_point *= 100
                break
        else:
            print("No horizontal reflection point found pruning start.")

        if reflection_point is None:
            for i in range(len(pattern)):
                reflection_point = find_horizontal_reflection_index(pattern[:-i])
                if reflection_point is not None:
                    reflection_point *= 100
                    break
            else:
                print("No horizontal reflection point found pruning end.")

        # rotate the pattern 90 degrees so we can use our horizontal reflection
        # check to find vertical reflection lines
        rotated_pattern = rotate(pattern)

        if reflection_point is None:
            for i in range(len(rotated_pattern)):
                reflection_point = find_horizontal_reflection_index(rotated_pattern[i:])
                if reflection_point is not None:
                    reflection_point += i
                    break
            else:
                print("No vertical reflection point found pruning start.")

        if reflection_point is None:
            for i in range(len(rotated_pattern)):
                reflection_point = find_horizontal_reflection_index(
                    rotated_pattern[:-i]
                )
                if reflection_point is not None:
                    break
            else:
                print("No vertical reflection point found pruning end.")

        if reflection_point is not None:
            print(f"Found reflection point: {reflection_point}")
            reflection_point_score += reflection_point

        print("----")

    print(reflection_point_score)
