import argparse
from dataclasses import dataclass

import regex as re


@dataclass
class ConditionRecord:
    # a list of springs and their status: '.' good, '#' broken, '?' unknown
    spring_status: str

    # list of sizes of contiguous broken springs (2 if two adjacent springs are
    # broken.)
    damaged_springs: list[str]


# map of spring_status & list of damaged_springs -> number of arrangements
arrangement_cache = {}


def make_key(spring_status: str, damaged_springs: list[str]):
    return f"{spring_status}||{','.join(damaged_springs)}"


def broken_spring_combinations(spring_status: str, damaged_springs: list[str], level=0):
    print(f"{'  ' * level} {spring_status}, {damaged_springs}")

    if not damaged_springs:
        if "#" not in spring_status:
            # we have a valid arrangement
            return 1
        else:
            # we still have bad springs to process, but our records say we don't.
            return 0

    # look for the next contiguous set of broken springs
    regex = re.compile("[?#]{" + damaged_springs[0] + "}")

    arrangements = 0
    for match in regex.finditer(spring_status, overlapped=True):
        # for each possible location that fits X broken springs, validate
        # another broken spring is not adjacent to it.
        start, end = match.span()
        if end < len(spring_status) and spring_status[end] == "#":
            continue
        if start > 0 and spring_status[start - 1] == "#":
            continue

        # We handle this case in the recursion call, but may as well also stop now
        if len(spring_status[end + 1 :]) == 0 and len(damaged_springs[1:]) > 0:
            continue

        # we have found a spot X broken springs could fit, followed by an end
        # of line, "." or a "?". We skip that spot as it can't be a broken
        # spring, and recurse to find the next batch of broken springs.
        key = make_key(spring_status[end + 1 :], damaged_springs[1:])
        if key not in arrangement_cache:
            arrangement_cache[key] = broken_spring_combinations(
                spring_status[end + 1 :], damaged_springs[1:], level + 1
            )
        else:
            print(f"{'  ' * level} - Cache hit for {key} = {arrangement_cache[key]}")

        arrangements += arrangement_cache[key]

    return arrangements


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="input.txt")
    args = parser.parse_args()

    filename = args.filename

    with open(filename) as f:
        file = f.read().splitlines()

    condition_records = []
    for row in file:
        spring_status, damaged_springs = row.split()
        damaged_springs_list = damaged_springs.split(",")
        condition_records.append(ConditionRecord(spring_status, damaged_springs_list))

    total_arrangements = []
    for cr in condition_records:
        print(f"Find solutions for {cr.spring_status} and {cr.damaged_springs}")
        arrangement = broken_spring_combinations(
            cr.spring_status, cr.damaged_springs, level=1
        )
        print(f"-> Arrangements: {arrangement}")
        print("---")
        total_arrangements.append(arrangement)

    print(sum(total_arrangements))
