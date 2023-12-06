import sys
import time
from collections import defaultdict
from dataclasses import dataclass

start_time = time.time()  # Start measuring execution time


@dataclass
class Mapping:
    destination_range: int
    source_range: int

    def __init__(self, destination, source, length):
        self.destination_range = range(destination, destination + length)
        self.source_range = range(source, source + length)


def extract_mappings(header, lines, ranges):
    # extract mappings from lines and store values in ranges
    header = header.strip(" map:")
    while mapping := lines.pop(0).strip():
        try:
            destination, source, length = mapping.split()
            ranges[header].append(Mapping(int(destination), int(source), int(length)))
        except ValueError:
            break


def parse_input_file(filename):
    ranges = defaultdict(list)

    with open(filename) as f:
        lines = f.readlines()

    # first line is the seeds
    seeds = [int(seed) for seed in lines.pop(0).strip().split("seeds: ")[1].split()]

    # toss blank line
    lines.pop(0)

    while lines:
        try:
            header = lines.pop(0).strip()
            extract_mappings(header, lines, ranges)
        except IndexError:
            break

    return seeds, ranges


def range_intersection(range1, range2):
    start = max(range1.start, range2.start)
    end = min(range1.stop, range2.stop)
    if start < end:
        return range(start, end)
    else:
        return None


def find_valid_locations(seed_ranges, ranges):
    mapping_names = ranges.keys()
    smallest_location = None

    for seed_range in seed_ranges:
        print(f"{seed_range.start} -> {seed_range.stop} ({len(seed_range)} seeds)")

        current_ranges, next_ranges = [seed_range], []

        for mapping_name in mapping_names:
            for current_range in current_ranges:
                # walk through the mapping tables for each range of values we
                # need to check

                for mapping in ranges[mapping_name]:
                    valid_range = range_intersection(
                        current_range, mapping.source_range
                    )

                    if valid_range:
                        # get zero indexed keys for the destination source mapping
                        start = valid_range.start - mapping.source_range.start
                        stop = valid_range.stop - mapping.source_range.start

                        # we have a valid range to check in our next list of mappings
                        next_ranges.append(
                            range(
                                mapping.destination_range.start + start,
                                mapping.destination_range.start + stop,
                            )
                        )

            if next_ranges:
                # we found valid mappings, so use them when checking the next
                # mapping table if next_ranges was empty, the original list of
                # mappings just map to themselves.
                current_ranges, next_ranges = next_ranges, []

        for current_range in current_ranges:
            # find the smallest location from all the valid ranges we ended up with.
            smallest_location = (
                min(smallest_location, current_range.start)
                if smallest_location
                else current_range.start
            )

    return smallest_location


def get_seed_ranges(seeds):
    seed_pairs = []
    while seeds:
        start = seeds.pop(0)
        end = seeds.pop(0)
        seed_pairs.append(range(start, start + end))
    return seed_pairs


filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

seeds, ranges = parse_input_file(filename)
seed_ranges = get_seed_ranges(seeds)

print(find_valid_locations(seed_ranges, ranges))

end_time = time.time()  # Stop measuring execution time
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")
