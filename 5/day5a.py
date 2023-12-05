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
    while True:
        mapping = lines.pop(0).strip()
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


def find_valid_locations(seeds, ranges):
    mapping_names = ranges.keys()
    valid_locations = []
    for seed in seeds:
        current, next = [seed], []
        for mapping_name in mapping_names:
            for i in current:
                for mapping in ranges[mapping_name]:
                    if i in mapping.source_range:
                        mapped_i = mapping.destination_range[
                            i - mapping.source_range.start
                        ]
                        next.append(mapped_i)
            if next:
                current, next = next, []

        valid_locations.extend(current)

    return valid_locations


seeds, ranges = parse_input_file("input.txt")

print(min(find_valid_locations(seeds, ranges)))

end_time = time.time()  # Stop measuring execution time
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")
