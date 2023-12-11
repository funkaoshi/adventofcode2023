import argparse
import itertools

from loguru import logger

Point = tuple[int, int]


class GalaxyMap:
    def __init__(self, image: list[list[str]], expansion_amount: int):
        self.image = image
        self.expansion_amount = expansion_amount
        self.galaxies = self.get_galaxies()
        self._expanded_rows = self.get_expanded_rows()
        self._expanded_cols = self.get_expanded_cols()

    def get_galaxies(self) -> list[Point]:
        return [
            (i, j)
            for i in range(len(self.image))
            for j in range(len(self.image[i]))
            if self.image[i][j] == "#"
        ]

    def get_expanded_rows(self) -> list[int]:
        return [i for i in range(len(self.image)) if "#" not in self.image[i]]

    def get_expanded_cols(self) -> list[int]:
        return [
            i
            for i in range(len(self.image[0]))
            if "#" not in [row[i] for row in self.image]
        ]

    def distance(self, a: Point, b: Point):
        h_a, h_b = sorted([a[1], b[1]])
        v_a, v_b = sorted([a[0], b[0]])

        expand_h = len([i for i in self._expanded_cols if i in range(h_a, h_b)])
        expand_v = len([i for i in self._expanded_rows if i in range(v_a, v_b)])

        horizontal_distance = h_b - h_a - expand_h + self.expansion_amount * expand_h
        vertical_distance = v_b - v_a - expand_v + self.expansion_amount * expand_v

        logger.debug(
            f"{a} -> {b} -> {horizontal_distance} + {vertical_distance} = "
            f"{horizontal_distance + vertical_distance}"
        )
        logger.debug(f" -> expand_h: {expand_h}")
        logger.debug(f" -> expand_v: {expand_v}")

        return vertical_distance + horizontal_distance

    def calculate_all_path_shortest_distances(self):
        return {
            pairs: self.distance(*pairs)
            for pairs in itertools.combinations(self.galaxies, 2)
        }

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="input.txt")
    parser.add_argument("-n", "--expansion_amount", action="store", default=1000000)
    args = parser.parse_args()

    filename = args.filename
    expansion_amount = int(args.expansion_amount)

    logger.debug(f"{filename=}, {expansion_amount=}")

    with open(filename) as f:
        image = [list(row) for row in f.read().splitlines()]

    galaxy_map = GalaxyMap(image, expansion_amount)
    distances = galaxy_map.calculate_all_path_shortest_distances()

    logger.info(sum(value for value in distances.values()))
