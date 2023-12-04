with open("input.txt") as f:
    lines = f.readlines()

cards = {}

# store the input in a dictionary: card_id -> {"winners": [], "numbers": [], "count": 1}
for line in lines:
    winners, numbers = line.split(" | ")
    card, winners = winners.split(":")
    card_id = int(card.split()[1])
    winners = [winner.strip() for winner in winners.strip().split() if winner]
    numbers = [number.strip() for number in numbers.strip().split() if number]

    cards[card_id] = {"winners": winners, "numbers": numbers, "count": 1}

for card_id, values in cards.items():
    winners, numbers, count = values["winners"], values["numbers"], values["count"]

    # calculate winners for each card we possess
    for x in range(count):
        next_card = card_id + 1

        for winner in winners:
            if winner in numbers:
                # we have a winning number, so we win an extra copy of the next card
                cards[next_card]["count"] += 1
                next_card += 1

# display the total number of cards we have
print(sum([value["count"] for _, value in cards.items()]))
