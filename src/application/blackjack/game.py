from src.domain.models import Deck, Card
from src.domain.player import Player, Dealer
from random import Random

class BlackJackGame:
    def __init__(self, player: Player, dealer: Dealer, table_min: int = 1, table_max: int = float('inf'), bj_payout: float = 1.5, rng: Random = None):
        # Validation Logic
        if player is None:
            raise ValueError("Player cannot be None")
        if dealer is None:
            raise ValueError("Dealer cannot be None")
        if table_min < 0:
            raise ValueError("Table minimum cannot be negative")
        if table_max < table_min:
            raise ValueError("Table maximum cannot be less than table minimum")
        if bj_payout not in (1.5, 6 / 5):
            raise ValueError("BlackJack Payout must be either 3/2 or 6/5")

        self.player = player
        self.dealer = dealer
        self.deck = Deck(rng=rng)
        self.discard = []
        self.current_bet = 0
        self.bj_payout = bj_payout
        self.table_min = table_min
        self.table_max = table_max

    def start_round(self, bet:int) -> None:
        if self.player.bankroll < self.table_min:
            raise ValueError("Bankroll cannot be less than table minimum, need to buy in")
        self.enter_bets(bet)
        self.deal_cards()

        if self.player.has_blackjack and self.dealer.has_blackjack:
            self.push()
        elif self.player.has_blackjack:
            self.player_wins(multiplier = (1 + self.bj_payout))
        elif self.dealer.has_blackjack:
            self.dealer_wins()

    def enter_bets(self, bet: int):
        if bet > self.table_max:
            raise ValueError("The bet cannot be greater than the table max")
        elif bet < self.table_min:
            raise ValueError("The bet cannot be less than the table min")
        self.current_bet += self.player.place_bet(bet)

    def deal_cards(self) -> None:
        for _ in range(2):
            self.player.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())

    def player_wins(self, multiplier:float = 2) -> None:
        self.player.resolve_outcome(multiplier * self.current_bet)
        self.end_round()

    def dealer_wins(self) -> None:
        self.dealer.resolve_outcome(self.current_bet)
        self.end_round()

    def push(self) -> None:
        self.player.resolve_outcome(self.current_bet)
        self.end_round()

    def end_round(self) -> None:
        self.player.reset_hand()
        self.dealer.reset_hand()
        self.current_bet = 0

    @property
    def dealer_showing(self) -> Card:
        return self.dealer.hand.cards[0]

    @property
    def dealer_hiding(self) -> Card:
        return self.dealer.hand.cards[1]
