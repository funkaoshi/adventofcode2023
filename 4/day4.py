from typing import List

with open("input.txt") as f:
    lines = f.readlines()

# store the winnings for each scratch card
total_winnings: List[int] = []

for line in lines:
    # split up each line into the winnnig numbers and the numbers on the card
    winners, numbers = line.split(" | ")
    winners = [winner.strip() for winner in winners.split(":")[1].strip().split() if winner]
    numbers = [number.strip() for number in numbers.strip().split() if number]

    # tally the number of winning numbers on the card
    winning_numbers = len([winner for winner in winners if winner in numbers])
    if not winning_numbers:
        continue

    # calculate the winnings for the card (doubling the winnings for each winning number)
    total_winnings.append(2 ** (winning_numbers-1))

print(sum(total_winnings))
