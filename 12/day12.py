import argparse
import cProfile
import io
import pstats
from dataclasses import dataclass

import regex as re
from loguru import logger


@dataclass
class ConditionRecord:
    # a list of springs and their status: '.' good, '#' broken, '?' unknown
    spring_status: str

    # list of sizes of contiguous broken springs (2 if two adjacent springs are
    # broken.)
    damaged_springs: list[str]


# map of spring_status & list of damaged_springs -> number of arrangements
arrangement_cache = {}
regex_cache = {}


def make_key(spring_status: str, damaged_springs: list[str]):
    return f"{spring_status}||{','.join(damaged_springs)}"


def broken_spring_combinations(
    spring_status: str, damaged_springs: list[str], current_arrangement="", level=0
) -> list[str]:
    if not damaged_springs:
        if "#" not in spring_status:
            return [current_arrangement + spring_status.replace("?", ".")]
        else:
            # we still have bad springs to process, but our records say we don't.
            return []

    # look for the next contiguous set of broken springs
    if damaged_springs[0] not in regex_cache:
        regex_cache[damaged_springs[0]] = re.compile("[?#]{" + damaged_springs[0] + "}")

    regex = regex_cache[damaged_springs[0]]

    arrangements = []
    for match in regex.finditer(spring_status, overlapped=True):
        start, end = match.span()

        # Broken springs proceed this match, so any subsequent match will be invalid.
        if "#" in spring_status[:start]:
            break

        # Broken springs adjacent to this match.
        if end < len(spring_status) and spring_status[end] == "#":
            continue
        if start > 0 and spring_status[start - 1] == "#":
            continue

        # We handle this case in the recursion call, but may as well also stop now.
        # We have matched the whole string, but have more damaged springs to process.
        if len(spring_status[end + 1 :]) == 0 and len(damaged_springs[1:]) > 0:
            continue

        next_arrangement = current_arrangement + (
            spring_status[:start].replace("?", ".") + "#" * int(damaged_springs[0])
        )
        next_arrangement += "." if end < len(spring_status) else ""

        # we have found a spot X broken springs could fit, followed by an end
        # of line, "." or a "?". We skip that spot as it can't be a broken
        # spring, and recurse to find the next batch of broken springs.
        key = make_key(spring_status[end + 1 :], damaged_springs[1:])
        if key not in arrangement_cache:
            arrangement_cache[key] = broken_spring_combinations(
                spring_status[end + 1 :],
                damaged_springs[1:],
                next_arrangement,
                level + 1,
            )

        arrangements += arrangement_cache[key]

    return arrangements


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

    pr = cProfile.Profile()
    pr.enable()

    total_arrangements = []
    for cr in condition_records:
        arrangements = broken_spring_combinations(
            cr.spring_status, cr.damaged_springs, level=1
        )
        total_arrangements.append(len(arrangements))

        logger.info(f"Found {len(arrangements)} arrangements for {cr.spring_status}")
        logger.info(f"Processed {len(total_arrangements)} of {len(condition_records)}")

    pr.disable()
    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

logger.info(f"Total: {sum(total_arrangements)}")
