import itertools
import sys

GalaxyMap = list[list[str]]
Node = tuple[int, int]

filename = "input.txt" if len(sys.argv) == 1 else sys.argv[1]

with open(filename) as f:
    file = f.read().splitlines()

galaxy_map = [list(row) for row in file]


def expanded_galaxy_map(galaxy: GalaxyMap) -> GalaxyMap:
    expanded_rows = []
    for row in galaxy:
        expanded_rows.append(row)
        if "#" not in row:
            expanded_rows.append(row)

    return expanded_rows


def rotate_galaxy_map(galaxy: GalaxyMap) -> GalaxyMap:
    rotated_galaxy_map = []
    for i in range(len(galaxy[0])):
        rotated_row = []
        for j in range(len(galaxy)):
            rotated_row.append(galaxy[j][i])

        rotated_galaxy_map.append(rotated_row)

    return rotated_galaxy_map


def get_galaxies(galaxy_map: GalaxyMap) -> list[Node]:
    return [
        (i, j)
        for i in range(len(galaxy_map))
        for j in range(len(galaxy_map[i]))
        if galaxy_map[i][j] == "#"
    ]


def manhattan_distance(node1: Node, node2: Node) -> int:
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


def calculate_all_path_shortest_distances(galaxies: list[Node]):
    distances = []
    for pairs in itertools.combinations(galaxies, 2):
        distances.append((pairs, manhattan_distance(*pairs)))
    return distances


# add extra rows/columns to the star map
galaxy_map = expanded_galaxy_map(galaxy_map)
galaxy_map = expanded_galaxy_map(rotate_galaxy_map(galaxy_map))
galaxy_map = rotate_galaxy_map(galaxy_map)

galaxies = get_galaxies(galaxy_map)
distances = calculate_all_path_shortest_distances(galaxies)
print(len(distances))
print(sum(value[1] for value in distances))
