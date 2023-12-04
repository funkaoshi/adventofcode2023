import re
from collections import defaultdict


GAME_RE = re.compile("Game (\d+)")
RED_RE = re.compile("(\d+) red")
BLUE_RE = re.compile("(\d+) blue")
GREEN_RE = re.compile("(\d+) green")

red = defaultdict(set)
blue = defaultdict(set)
green = defaultdict(set)

powers = []

with open("input.txt") as f:
    for line in f:
        game = line.split(":")
        game_num = int(GAME_RE.match(game[0]).group(1))

        rounds = game[1].split(";")

        # track the minimum number of balls of each colour required for in each game
        minimum_balls = {"red": 0, "blue": 0, "green": 0}

        for round in rounds:
            red_balls = RED_RE.search(round)
            blue_balls = BLUE_RE.search(round)
            green_balls = GREEN_RE.search(round)

            red_balls = int(red_balls[1]) if red_balls else 0
            blue_balls = int(blue_balls[1]) if blue_balls else 0
            green_balls = int(green_balls[1]) if green_balls else 0

            if red_balls > minimum_balls["red"]:
                minimum_balls["red"] = red_balls
            if blue_balls > minimum_balls["blue"]:
                minimum_balls["blue"] = blue_balls
            if green_balls > minimum_balls["green"]:
                minimum_balls["green"] = green_balls

        powers.append(
            minimum_balls["red"] * minimum_balls["blue"] * minimum_balls["green"]
        )

print(sum(powers))
