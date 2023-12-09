import sys
from itertools import pairwise


def find_sequence_differences(sequence: list[int]) -> dict[int, list[int]]:
    level = 0
    sequence_differences = {level: sequence}
    while True:
        sequence_differences[level + 1] = [
            y - x for x, y in pairwise(sequence_differences[level])
        ]

        if all(i == 0 for i in sequence_differences[level + 1]):
            break

        level += 1

    return sequence_differences


def find_next_value(sequence_differences: dict[int, list[int]]) -> int:
    for i in range(len(sequence_differences) - 1, 0, -1):
        top_element = sequence_differences[i][-1]
        last_element = sequence_differences[i - 1][-1]
        sequence_differences[i - 1].append(last_element + top_element)

    return sequence_differences[0][-1]


filename = "input.txt" if len(sys.argv) == 1 else sys.argv[1]

with open(filename) as f:
    raw_sequences = f.read().splitlines()

sequences = [[int(n) for n in s.split()] for s in raw_sequences]

next_values = []
previous_values = []
for sequence in sequences:
    next_values.append(find_next_value(find_sequence_differences(sequence)))

    # for part 2 of the problem we find the next number in the reversed sequence.
    previous_values.append(find_next_value(find_sequence_differences(sequence[::-1])))

print(sum(next_values))
print(sum(previous_values))
