from dataclasses import dataclass
from enum import Enum

card_values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


class HandType(Enum):
    QUANT = 7
    QUAD = 6
    FULL_HOUSE = 5
    TRIPPLE = 4
    TWO_PAIR = 3
    PAIR = 2
    HIGH_CARD = 1


@dataclass
class HandBid:
    cards: str
    sorted_cards: str
    cards_values: list[int]
    hand_type: HandType
    bid: int
    rank: int = 0
    winnings: int = 0


def classify_hand(cards):
    """Classify a sorted set of cards into one of the 7 types of hands"""

    # cards is a 5 digit string [0 1 2 3 4]

    if cards[0] == cards[4]:
        # first and last card are the same, so all cards are the same
        return HandType.QUANT
    elif cards[0] == cards[3] or cards[1] == cards[4]:
        # first 4 or last 4 cards are the same, so 4 cards are the same
        return HandType.QUAD
    elif (
        cards[0] == cards[1]
        and cards[2] == cards[4]
        or cards[0] == cards[2]
        and cards[3] == cards[4]
    ):
        # first 2 and last 3 or first 3 and last 2 cards are the same,
        # so we have a full house.
        return HandType.FULL_HOUSE
    elif cards[0] == cards[2] or cards[1] == cards[3] or cards[2] == cards[4]:
        # first 3, middle 3, or last 3 cards are the same, so 3 cards are the same
        return HandType.TRIPPLE
    elif (
        cards[0] == cards[1]
        and cards[2] == cards[3]
        or cards[1] == cards[2]
        and cards[3] == cards[4]
        or cards[0] == cards[1]
        and cards[3] == cards[4]
    ):
        return HandType.TWO_PAIR
    elif (
        cards[0] == cards[1]
        or cards[1] == cards[2]
        or cards[2] == cards[3]
        or cards[3] == cards[4]
    ):
        return HandType.PAIR
    else:
        return HandType.HIGH_CARD


def load_hands(filename="input.txt"):
    with open(filename) as f:
        lines = f.readlines()

    hands = []
    for line in lines:
        cards, bid = line.split()
        sorted_cards = "".join(sorted(list(cards), key=lambda x: -card_values[x]))
        cards_values = [card_values[card] for card in cards]
        hand_type = classify_hand(sorted_cards)
        hands.append(HandBid(cards, sorted_cards, cards_values, hand_type, int(bid)))

    sorted_hands = sorted(hands, key=lambda x: (x.hand_type.value, x.cards_values))
    for i, hand in enumerate(sorted_hands, start=1):
        hand.rank = i
        hand.winnings = hand.rank * hand.bid

        print(hand.rank, hand.cards, hand.hand_type.name)

    return sorted_hands


hands = load_hands("input.txt")
total_winnings = sum([hand.winnings for hand in hands])
print(total_winnings)
