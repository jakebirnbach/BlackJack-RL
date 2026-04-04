from application.strategies.base_strategy import BaseStrategy
from domain.constants import Action, Outcome
from domain.models import Deck, Card, GameState
from domain.player import Player, Dealer
from random import Random

class BlackJackGame:
    def __init__(self, player: Player, dealer: Dealer, num_decks: int = 1, stand_17: bool = True,table_min: int = 1, table_max: float = float('inf'), bj_payout: float = 1.5, rng: Random = None):
        # Validation Logic
        if player is None:
            raise ValueError("Player cannot be None")
        if dealer is None:
            raise ValueError("Dealer cannot be None")
        if num_decks <= 0:
            raise ValueError("Number of decks must be greater than 0")
        if table_min < 0:
            raise ValueError("Table minimum cannot be negative")
        if table_max < table_min:
            raise ValueError("Table maximum cannot be less than table minimum")
        if bj_payout not in (1.5, 6 / 5):
            raise ValueError("BlackJack Payout must be either 3/2 or 6/5")

        self.player = player
        self.dealer = dealer
        self.deck = Deck(num_decks=num_decks,rng=rng)
        self.discard = []
        self.current_bet = 0
        self.stand_on_17 = stand_17
        self.bj_payout = bj_payout
        self.table_min = table_min
        self.table_max = table_max

    def start_round(self, bet:int) -> Outcome | None:
        if self.player.bankroll < self.table_min:
            raise ValueError("Bankroll cannot be less than table minimum, need to buy in")
        self.enter_bets(bet)
        self.deal_cards()

        if self.player.has_blackjack and self.dealer.has_blackjack:
            self.push()
            return Outcome.PUSH
        elif self.player.has_blackjack:
            self.player_wins(multiplier = (1 + self.bj_payout))
            return Outcome.PLAYER_WIN
        elif self.dealer.has_blackjack:
            self.dealer_wins()
            return Outcome.DEALER_WIN
        return None

    def enter_bets(self, bet: int) -> None:
        if bet > self.table_max:
            raise ValueError("The bet cannot be greater than the table max")
        elif bet < self.table_min:
            raise ValueError("The bet cannot be less than the table min")
        self.current_bet += self.player.place_bet(bet)

    def deal_cards(self) -> None:
        for _ in range(2):
            self.player.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())

    def dealer_turn(self) -> Outcome:
        while self.dealer.hand.value < 17 or (
                not self.stand_on_17 and self.dealer.hand.value == 17 and self.dealer.hand.is_soft):
            self.dealer.hit(self.deck.deal())
            if self.dealer.busted:
                self.player_wins()
                return Outcome.PLAYER_WIN
        if self.dealer.hand.value > self.player.hand.value:
            self.dealer_wins()
            return Outcome.DEALER_WIN
        elif self.dealer.hand.value < self.player.hand.value:
            self.player_wins()
            return Outcome.PLAYER_WIN
        else:
            self.push()
            return Outcome.PUSH

    def player_turn(self, player_strategy: BaseStrategy)-> Outcome | None:
        while True:
            curr_state = GameState(
                player_value=self.player.hand.value,
                is_soft=self.player.hand.is_soft,
                dealer_showing=self.dealer_showing.rank.points,
                bankroll=self.player.bankroll,
                current_bet=self.current_bet
            )
            action = player_strategy.action(curr_state)
            if action == Action.STAND:
                break
            elif action == Action.HIT:
                self.player.hit(self.deck.deal())
                if self.player.busted:
                    self.dealer_wins()
                    return Outcome.DEALER_WIN
            elif action == Action.DOUBLE_DOWN:
                if len(self.player.hand.cards) != 2:
                    raise ValueError("Can only double down on initial hand")
                self.enter_bets(self.current_bet)
                self.player.hit(self.deck.deal())
                if self.player.busted:
                    self.dealer_wins()
                    return Outcome.DEALER_WIN
                break

            else:
                raise ValueError(f"Invalid action: {action}")
        return None

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
        self.discard.extend(self.player.hand.clear())
        self.discard.extend(self.dealer.hand.clear())
        self.current_bet = 0

    @property
    def dealer_showing(self) -> Card:
        return self.dealer.hand.cards[0]

    @property
    def dealer_hiding(self) -> Card:
        return self.dealer.hand.cards[1]
