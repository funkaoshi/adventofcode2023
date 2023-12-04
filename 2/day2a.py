import re

GAME_RE = re.compile("Game (\d+)")
RED_RE = re.compile("(\d+) red")
BLUE_RE = re.compile("(\d+) blue")
GREEN_RE = re.compile("(\d+) green")

MAX_RED_BALLS = 12
MAX_GREEN_BALLS = 13
MAX_BLUE_BALLS = 14

# games that have no rounds with more than the maximum number of balls of any colour
valid_games = set()

with open("input.txt") as f:
    for line in f:
        # extract the game number and the details of the rounds played in the game
        game = line.split(":")
        game_num = int(GAME_RE.match(game[0]).group(1))
        rounds = game[1].split(";")

        valid_game = True
        for round in rounds:
            # extract the number of balls of each colour from the round
            red_balls = RED_RE.search(round)
            blue_balls = BLUE_RE.search(round)
            green_balls = GREEN_RE.search(round)

            red_balls = int(red_balls[1]) if red_balls else 0
            blue_balls = int(blue_balls[1]) if blue_balls else 0
            green_balls = int(green_balls[1]) if green_balls else 0

            # if any of the balls exceed the maximum number of balls of that colour,
            # the game is invalid.
            if (
                red_balls > MAX_RED_BALLS
                or blue_balls > MAX_BLUE_BALLS
                or green_balls > MAX_GREEN_BALLS
            ):
                valid_game = False
                break

        if valid_game:
            valid_games.add(game_num)

print(sum(valid_games))
