from .models import Card, Hand


class Player:
    def __init__(self, bankroll: float):
        if bankroll < 0:
            raise ValueError("bankroll cannot be negative")
        self.bankroll = bankroll
        self.reset_hand()

    def reset_hand(self) -> None:
        self.hand : Hand = Hand()

    def place_bet(self, bet: int) -> int:
        if bet > self.bankroll:
            raise ValueError("The bet cannot be greater than the bankroll")
        elif bet <= 0:
            raise ValueError("The bet cannot be less than 0")
        self.bankroll -= bet
        return bet

    def resolve_outcome(self, payout: float) -> None:
        self.bankroll += payout

    def hit(self, card: Card) -> None:
        self.hand.add_card(card)

    def stand(self) -> None:
        pass

    @property
    def has_blackjack(self) -> bool:
        return self.hand.is_blackjack

    @property
    def busted(self) -> bool:
        return self.hand.is_bust

    def buy_in(self, value:int) -> None:
        if value <= 0:
            raise ValueError("The value cannot be less than 0")
        self.bankroll += value

class Dealer(Player):
    def __init__(self, bankroll: float, stand_on_17: bool = True):
        super().__init__(bankroll)
        self.stand_on_17 = stand_on_17