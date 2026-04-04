import random
from application.blackjack.game import BlackJackGame
from application.strategies.base_strategy import BaseStrategy
from domain.constants import Outcome


class GameOrchestrator:
    def __init__(self, game: BlackJackGame, strategy: BaseStrategy):
        self.cut_point = None
        self.game: BlackJackGame = game
        self.player_strategy: BaseStrategy = strategy
        self.cut_deck()

    def play_hand(self, bet: int) -> Outcome:
        start_game = self.game.start_round(bet)
        if start_game:
            return start_game

        player_turn = self.game.player_turn(self.player_strategy)
        if player_turn:
            return player_turn

        return self.game.dealer_turn()

    def play_shoe(self, bet: int) -> list[Outcome]:
        hand_outcomes: list[Outcome] = []
        while len(self.game.discard) < self.cut_point:
            hand_outcomes.append(self.play_hand(bet))

        self.game.discard.clear()
        self.game.deck.reset()
        self.cut_deck()
        return hand_outcomes

    def cut_deck(self) -> None:
        self.cut_point = int(random.uniform(0.6, 0.8) * len(self.game.deck.cards))






