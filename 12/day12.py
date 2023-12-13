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
cache_hits = 0


# compile one regex for each size of contiguous damaged springs we encounter.
regex_cache = {}


def broken_spring_combinations(spring_status: str, damaged_springs: list[str]) -> int:
    if not damaged_springs:
        if "#" not in spring_status:
            # We have a valid arrangement!
            return 1
        else:
            # We still have damaged springs to process, but our records say we don't.
            return 0

    # look for the next contiguous set of broken springs
    if damaged_springs[0] not in regex_cache:
        regex_cache[damaged_springs[0]] = re.compile("[?#]{" + damaged_springs[0] + "}")

    regex = regex_cache[damaged_springs[0]]

    arrangements = 0
    for match in regex.finditer(spring_status, overlapped=True):
        start, end = match.span()

        # One or more broken springs proceed this match so this match and
        # any subsequent match will be invalid.
        if "#" in spring_status[:start]:
            break

        # There are broken springs adjacent to this match so it's invalid.
        if end < len(spring_status) and spring_status[end] == "#":
            continue
        if start > 0 and spring_status[start - 1] == "#":
            continue

        # We have matched the whole string, but have more damaged springs to process.
        # We handle this case in the recursion call, but may as well also stop now.
        if len(spring_status[end + 1 :]) == 0 and len(damaged_springs[1:]) > 0:
            continue

        # We have a valid match. The next value must be a '." or the end of the string,
        # so we assume as much when continuing on in finding our arrangements. (We will
        # turn a '?' into a '.')
        key = f"{spring_status[end + 1 :]}||{damaged_springs[1:]}"
        if key not in arrangement_cache:
            arrangement_cache[key] = broken_spring_combinations(
                spring_status[end + 1 :],
                damaged_springs[1:],
            )
        else:
            global cache_hits
            cache_hits += 1

        arrangements += arrangement_cache[key]

    return arrangements


def find_total_arrangements(condition_records: list[ConditionRecord]) -> int:
    total_arrangements = []
    for cr in condition_records:
        arrangements = broken_spring_combinations(cr.spring_status, cr.damaged_springs)
        total_arrangements.append(arrangements)

        print(f"Found {arrangements} arrangements for {cr.spring_status}")
        print(f"Processed {len(total_arrangements)} of {len(condition_records)}")

    return sum(total_arrangements)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="input.txt")
    parser.add_argument("-c", "--copies", action="store", default=0, type=int)
    args = parser.parse_args()

    filename = args.filename
    copies = args.copies

    with open(filename) as f:
        file = f.read().splitlines()

    condition_records = []
    for row in file:
        spring_status, damaged_springs = row.split()
        damaged_springs_list = damaged_springs.split(",")
        if copies > 0:
            spring_status = "?".join([spring_status] * copies)
            damaged_springs_list = damaged_springs_list * copies
        condition_records.append(ConditionRecord(spring_status, damaged_springs_list))

    total_arrangements = find_total_arrangements(condition_records)

    print(f"Total: {total_arrangements}")
    print(f"Cache hits: {cache_hits}    Cache size: {len(arrangement_cache)}")
