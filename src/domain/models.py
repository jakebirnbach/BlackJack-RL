from __future__ import annotations
from .constants import Suit, Rank
from random import Random


class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{str(self.rank.name).capitalize()} of {self.suit.value}"


class Deck:
    def __init__(self, rng: Random | None = None):
        self.cards: list[Card] = []
        self._rng = rng or Random()
        self.reset()

    def shuffle(self) -> None:
        self._rng.shuffle(self.cards)

    def deal(self) -> Card:
        if not self.cards:
            raise ValueError("Deck is empty")
        return self.cards.pop()

    def reset(self) -> None:
        self.cards: list[Card] = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))
        self.shuffle()

class Hand:
    def __init__(self):
        self.cards: list[Card] = []
        self.value: int = 0
        self._aces: int = 0

    def add_card(self, card: Card):
        if card is None:
            raise ValueError("Card is empty")

        self.cards.append(card)
        self.value += card.rank.points

        if card.rank == Rank.ACE:
            self._aces += 1

        # Dynamically recomputes the best hand if we have aces
        while self.value > 21 and self._aces > 0:
            self._aces -= 1
            self.value -= 10

    @property
    def is_soft(self) -> bool:
        return self._aces > 0

    @property
    def is_bust(self) -> bool:
        return self.value > 21

    @property
    def is_blackjack(self) -> bool:
        return self.value == 21 and len(self.cards) == 2

    @property
    def usable_ace(self) -> bool:
        return self._aces > 0

    def __str__(self) -> str:
        cards_str = ", ".join(str(card) for card in self.cards)
        return f"[{cards_str}] (value: {self.value})"