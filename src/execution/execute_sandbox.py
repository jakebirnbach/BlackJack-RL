from typing import Final

from application.strategies.base_strategy import BaseStrategy
from domain.models import OutcomeOutput, OutputStats
from domain.player import Player, Dealer
from application.blackjack.game import BlackJackGame
from application.blackjack.game_orchestrator import GameOrchestrator
from application.strategies.hit17_strategy import Hit17Strategy
from application.reporting.stats import StatCalculator

NUM_SHOES: Final = 10000
NUM_DECKS: Final = 6
STARTING_BANKROLL: Final = 1000
PLAYER_STRATEGY: BaseStrategy = Hit17Strategy()
BET_AMOUNT: Final = 25

def execute_sandbox():
    result_stats: list[OutputStats] = []
    for num in range(NUM_SHOES):
        if num % 1000 == 0:
            print(f"Processing shoe {num} of {NUM_SHOES}")
        player: Player = Player(STARTING_BANKROLL)
        dealer: Dealer = Dealer(1000000)
        game: BlackJackGame = BlackJackGame(player, dealer, num_decks=NUM_DECKS)
        orchestrator: GameOrchestrator = GameOrchestrator(game, PLAYER_STRATEGY)
        results: list[OutcomeOutput] = orchestrator.play_shoe(bet=BET_AMOUNT)
        hand_stats = StatCalculator.calculate_stats(results, STARTING_BANKROLL, player.bankroll)
        result_stats.append(hand_stats)

    aggregate_stats = StatCalculator.calculate_aggregate_stats(result_stats)
    print(aggregate_stats)
