import argparse
import itertools
from dataclasses import dataclass

import numpy as np

INTERVAL = range(200000000000000, 400000000000001)


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int


Velocity = Point


@dataclass(frozen=True)
class Trajectory:
    initial: Point
    velocity: Velocity


def parse_file(file):
    trajectories = []
    for line in file:
        raw_point, raw_vector = line.split(" @ ")
        point = Point(*[int(x) for x in raw_point.split(", ")])
        velocity = Velocity(*[int(x) for x in raw_vector.split(", ")])
        trajectories.append(Trajectory(point, velocity))
    return trajectories


def line_intersection_2D(t1: Trajectory, t2: Trajectory) -> Point | None:
    x1, y1 = t1.initial.x, t1.initial.y
    x2, y2 = t1.initial.x + t1.velocity.x, t1.initial.y + t1.velocity.y
    x3, y3 = t2.initial.x, t2.initial.y
    x4, y4 = t2.initial.x + t2.velocity.x, t2.initial.y + t2.velocity.y

    # check if lines are parallel
    if np.cross([x2 - x1, y2 - y1], [x4 - x3, y4 - y3]) == 0:
        return None

    # calculate intersection point
    t = np.cross([x3 - x1, y3 - y1], [x4 - x3, y4 - y3]) / np.cross(
        [x2 - x1, y2 - y1], [x4 - x3, y4 - y3]
    )

    return Point(x1 + t * (x2 - x1), y1 + t * (y2 - y1), 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="test.txt")
    args = parser.parse_args()

    filename = args.filename

    with open(filename) as f:
        file = f.read().splitlines()

    trajectories = parse_file(file)

    intersections = []
    for t1, t2 in itertools.combinations(trajectories, 2):
        print(f"{t1.initial.x}, {t1.initial.y} & {t2.initial.x}, {t2.initial.y}")

        intersection = line_intersection_2D(t1, t2)

        if intersection is None:
            print(" -> No intersection")
            continue

        print(f" -> Intersection at {intersection.x:0.2f}, {intersection.y:0.2f}")

        if (
            intersection.x < INTERVAL.start
            or intersection.y < INTERVAL.start
            or intersection.x > INTERVAL.stop
            or intersection.y > INTERVAL.stop
        ):
            print("   -> Intersection not in interval")
            continue

        if (
            (t1.velocity.x > 0 and intersection.x < t1.initial.x)
            or (t1.velocity.x < 0 and intersection.x > t1.initial.x)
            or (t2.velocity.x > 0 and intersection.x < t2.initial.x)
            or (t2.velocity.x < 0 and intersection.x > t2.initial.x)
        ):
            print("   -> Intersection before start")
            continue

        intersections.append(intersection)

    print(len(intersections))
