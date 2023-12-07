from dataclasses import dataclass
from enum import Enum

# map card to its numeric value in the game
card_values = {c: i for i, c in enumerate(list("23456789TJQKA"), start=2)}


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
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

    # if we have fewer than 5 cards we have some number of wildcards.
    num_cards = len(cards)

    if num_cards == 0 or num_cards == 1:
        # we have all jokers, or one card and 4 jokers, so we can make a five of a kind.
        return HandType.FIVE_OF_A_KIND

    if num_cards == 2:
        # we have 3 jokers, so we can turn a pair into a five of a kind,
        # or anything else into a four of a kind.
        if cards[0] == cards[1]:
            return HandType.FIVE_OF_A_KIND
        else:
            return HandType.FOUR_OF_A_KIND

    if num_cards == 3:
        # we have 2 jokers, so we can turn a tripple into a five of a kind, a pair
        # into a four of a kind, or anything else into a three of a kind.
        if cards[0] == cards[2]:
            return HandType.FIVE_OF_A_KIND
        elif cards[0] == cards[1] or cards[1] == cards[2]:
            return HandType.FOUR_OF_A_KIND
        else:
            return HandType.TRIPPLE

    if num_cards == 4:
        if cards[0] == cards[3]:
            # Four of a kind becomes five of a kind
            return HandType.FIVE_OF_A_KIND
        elif cards[0] == cards[2] or cards[1] == cards[3]:
            # Three of a kind becomes four of a kind
            return HandType.FOUR_OF_A_KIND
        elif cards[0] == cards[1] and cards[2] == cards[3]:
            # Two pair becomes a full house
            return HandType.FULL_HOUSE
        elif cards[0] == cards[1] or cards[1] == cards[2] or cards[2] == cards[3]:
            # One pair becomes three of a kind
            return HandType.TRIPPLE
        else:
            return HandType.PAIR

    # ... else we have no wild cards

    if cards[0] == cards[4]:
        # first and last card are the same, so all cards are the same
        return HandType.FIVE_OF_A_KIND
    elif cards[0] == cards[3] or cards[1] == cards[4]:
        # first 4 or last 4 cards are the same, so 4 cards are the same
        return HandType.FOUR_OF_A_KIND
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


def load_hands(filename="input.txt", with_jokers=False):
    with open(filename) as f:
        lines = f.readlines()

    hands = []
    for line in lines:
        cards, bid = line.split()

        # convert cards into their values for sorting later. If we are playing with
        # jokers then their value is 1, not 11.
        cards_values = [
            1 if with_jokers and card == "J" else card_values[card] for card in cards
        ]

        # classify the hand: if we are playing with jokers then we remove them first.
        classify_cards = cards.replace("J", "") if with_jokers else cards
        sorted_cards = "".join(
            sorted(list(classify_cards), key=lambda x: -card_values[x])
        )
        hand_type = classify_hand(sorted_cards)

        hands.append(HandBid(cards, sorted_cards, cards_values, hand_type, int(bid)))

    sorted_hands = sorted(hands, key=lambda x: (x.hand_type.value, x.cards_values))
    for i, hand in enumerate(sorted_hands, start=1):
        hand.rank = i
        hand.winnings = hand.rank * hand.bid

    return sorted_hands


problem_one_winnings = sum([hand.winnings for hand in load_hands("input.txt")])
print(f"Problem 1: {problem_one_winnings == 250058342}")

problem_two_winnings = sum(
    [hand.winnings for hand in load_hands("input.txt", with_jokers=True)]
)
print(f"Problem 2: {problem_two_winnings == 250506580}")