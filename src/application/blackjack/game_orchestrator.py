from typing import Callable

from application.blackjack.game import BlackJackGame
from domain.constants import Action
from domain.models import GameState


class GameOrchestrator:
    def __init__(self, game: BlackJackGame, get_action: Callable[[GameState], Action], num_rounds: int = 1):
        self.game: BlackJackGame = game
        self.get_action: Callable[[GameState], Action] = get_action
    #
    # def play_round(self):




