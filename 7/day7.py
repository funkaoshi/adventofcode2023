import sys
from collections import Counter
from dataclasses import dataclass

HAND_SIZE = 5


@dataclass
class HandBid:
    cards: str
    bid: int

    # static variable stores map of card to its numeric value in the game
    card_values = {c: i for i, c in enumerate(list("23456789TJQKA"), start=2)}

    def key(self, with_jokers=False) -> tuple[tuple, tuple]:
        """key used to sort HandBid"""
        # if we are playing with jokers they are worth 1 not 11.
        values = tuple(
            1 if with_jokers and card == "J" else HandBid.card_values[card]
            for card in self.cards
        )
        return (self.classify_hand(with_jokers), values)

    def classify_hand(self, with_jokers: bool) -> tuple:
        """Classify a sorted set of cards into one of the 7 types of hands"""

        # if we are playing with jokers remove them from the hand
        cards = self.cards.replace("J", "") if with_jokers else self.cards

        # group are cards into matching sets, i.e. 22KKA -> (2, 2, 1). Shout out
        # to Victor for pointing out this simpler approach to classifying hands!
        card_groups = sorted(
            [count for _, count in Counter(cards).items()], reverse=True
        )
        if not card_groups:
            # handle the case we have nothing but wildcards
            card_groups = [0]

        # if we have fewer than 5 cards we have some wildcards. because this
        # is a simpler version of poker, we can improve our hand by simply
        # increase the size of our first match group: (2,2) -> (3,2);
        # (1,) -> (5,), (1,1,1,1) -> (2,1,1,1), etc.
        wildcards = HAND_SIZE - len(cards)
        card_groups[0] = card_groups[0] + wildcards

        return tuple(card_groups)


def load_hands(filename="input.txt") -> list[HandBid]:
    with open(filename) as f:
        lines = f.readlines()

    hands = []
    for line in lines:
        cards, bid = line.split()
        hands.append(HandBid(cards, int(bid)))

    return hands


def score_game(hands: list[HandBid], with_jokers=False) -> int:
    sorted_hands = sorted(hands, key=lambda x: x.key(with_jokers))
    total_winnings = [i * hand.bid for i, hand in enumerate(sorted_hands, start=1)]
    return sum(total_winnings)


filename = "input.txt" if len(sys.argv) == 1 else sys.argv[1]

hands = load_hands(filename)

problem_one_winnings = score_game(hands)
problem_two_winnings = score_game(hands, with_jokers=True)

print(f"Problem 1: {problem_one_winnings} - {problem_one_winnings == 250058342}")
print(f"Problem 2: {problem_two_winnings} - {problem_two_winnings == 250506580}")
