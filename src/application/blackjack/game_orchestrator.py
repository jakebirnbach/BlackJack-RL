import random
from application.blackjack.game import BlackJackGame
from application.strategies.base_strategy import BaseStrategy
from domain.constants import Outcome, Action
from domain.models import OutcomeOutput, GameState


class GameOrchestrator:
    def __init__(self, game: BlackJackGame, strategy: BaseStrategy) -> None:
        self.cut_point: int = 0
        self.game: BlackJackGame = game
        self.player_strategy: BaseStrategy = strategy
        self.cut_deck()

    def play_hand(self, bet: int) -> OutcomeOutput:
        start_game: OutcomeOutput | None = self.game.start_round(bet)
        if isinstance(start_game, OutcomeOutput):
            return start_game

        player_turn: OutcomeOutput | list[tuple[GameState, Action]] = self.game.player_turn(self.player_strategy)
        if isinstance(player_turn, OutcomeOutput):
            return player_turn

        return self.game.dealer_turn(player_turn)

    def play_shoe(self, bet: int) -> list[OutcomeOutput]:
        hand_outcomes: list[OutcomeOutput] = []
        while len(self.game.discard) < self.cut_point:
            hand_outcomes.append(self.play_hand(bet))

        self.game.discard.clear()
        self.game.deck.reset()
        self.cut_deck()
        return hand_outcomes

    def cut_deck(self) -> None:
        self.cut_point: int = int(random.uniform(0.6, 0.8) * len(self.game.deck.cards))






