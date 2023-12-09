import sys


def find_sequence_differences(sequence: list[str]) -> dict[int, list[int]]:
    level = 0
    sequence_differences = {level: sequence}
    while True:
        sequence_differences[level + 1] = [
            sequence_differences[level][i + 1] - sequence_differences[level][i]
            for i in range(len(sequence_differences[level]) - 1)
        ]

        if all(i == 0 for i in sequence_differences[level + 1]):
            break

        level += 1

    return sequence_differences


def find_next_value(sequence_differences: dict[int, list[int]]) -> int:
    for i in range(len(sequence_differences) - 1, 0, -1):
        top_element = sequence_differences[i][-1]
        last_element = sequence_differences[i - 1][-1]
        print(f"{top_element=}, {last_element=}")
        sequence_differences[i - 1].append(last_element + top_element)

    print(f"Next value: {sequence_differences[0][-1]}")

    return sequence_differences[0][-1]


def find_proceeding_value(sequence_differences: dict[int, list[int]]) -> int:
    for i in range(len(sequence_differences) - 1, 0, -1):
        top_element = sequence_differences[i][0]
        first_element = sequence_differences[i - 1][0]
        print(f"{i}: {top_element=}, {first_element=}")
        sequence_differences[i - 1].insert(0, first_element - top_element)

    print(f"Proceeding value: {sequence_differences[0][0]}")

    return sequence_differences[0][0]


filename = "input.txt" if len(sys.argv) == 1 else sys.argv[1]

with open(filename) as f:
    raw_sequences = f.read().splitlines()

sequences = [[int(n) for n in s.split()] for s in raw_sequences]

next_values = []
previous_values = []
for sequence in sequences:
    diffs = find_sequence_differences(sequence)
    next_values.append(find_next_value(diffs))
    previous_values.append(find_proceeding_value(diffs))

print(sum(next_values))
print(sum(previous_values))
