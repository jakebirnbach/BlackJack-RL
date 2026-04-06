from __future__ import annotations
from dataclasses import dataclass
from domain.constants import Suit, Rank, Outcome, Action
from random import Random


class Card:
    def __init__(self, rank: Rank, suit: Suit, num_decks: int = 1) -> None:
        self.rank: Rank = rank
        self.suit: Suit = suit
        self.num_decks: int = num_decks

    def __str__(self) -> str:
        return f"{str(self.rank.name).capitalize()} of {self.suit.value}"

class Deck:
    def __init__(self, num_decks: int = 1, rng: Random | None = None) -> None:
        if num_decks < 1:
            raise ValueError("Must be instantiated with at least 1 deck")

        self.num_decks: int = num_decks
        self.cards: list[Card] = []
        self._rng: Random = rng or Random()
        self.reset()

    def shuffle(self) -> None:
        self._rng.shuffle(self.cards)

    def deal(self) -> Card:
        if not self.cards:
            raise ValueError("Deck is empty")
        return self.cards.pop()

    def reset(self) -> None:
        self.cards: list[Card] = []
        for deck_num in range(1, self.num_decks + 1):
            for suit in Suit:
                for rank in Rank:
                    self.cards.append(Card(rank, suit, deck_num))
        self.shuffle()

class Hand:
    def __init__(self) -> None:
        self.cards: list[Card] = []
        self.value: int = 0
        self._aces: int = 0

    def add_card(self, card: Card) -> None:
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

    def clear(self) -> list[Card]:
        cards: list[Card] = self.cards
        self.cards: list[Card] = []
        self.value: int = 0
        self._aces: int = 0
        return cards

    @property
    def is_soft(self) -> bool:
        return self._aces > 0

    @property
    def is_bust(self) -> bool:
        return self.value > 21

    @property
    def is_blackjack(self) -> bool:
        return self.value == 21 and len(self.cards) == 2

    def __str__(self) -> str:
        cards_str: str = ", ".join(str(card) for card in self.cards)
        return f"[{cards_str}] (value: {self.value})"

@dataclass(frozen=True)
class GameState:
    player_value: int
    is_soft: bool
    dealer_showing: int
    bankroll: float
    current_bet: int

@dataclass
class OutcomeOutput:
    outcome: Outcome
    actions: list[tuple[GameState, Action]] # list of game states, and their resulting action
    bet_amount: int
    payout: float

@dataclass
class OutputStats:
    starting_bankroll: float
    ending_bankroll: float
    hands_played: int
    wins: int
    losses: int
    pushes: int
    total_wagered: float
    total_payout:float
    profit: float
    roi: float
    win_rate: float
    average_bet_amt: float