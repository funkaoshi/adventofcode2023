from dataclasses import dataclass


@dataclass
class Race:
    time: int  # length of race in ms
    distance: int  # the record winning distance in mm


with open("input.txt") as f:
    lines = f.readlines()

times = lines[0].strip().replace(" ", "").split(":")
distances = lines[1].strip().replace(" ", "").split(":")
races = [
    Race(int(time), int(distance)) for time, distance in zip(times[1:], distances[1:])
]

score = 1
for i, race in enumerate(races):
    winning_times = 0

    # speed corresponds 1-1 with how long you hold the button down
    # at the start of the race. We travel at that speed for the
    # remainder of the race.
    for speed in range(race.time):
        remaing_time = race.time - speed
        distance = speed * remaing_time

        if distance > race.distance:
            winning_times += 1

    score *= winning_times

print(score)
