from typing import Final

from application.strategies.base_strategy import BaseStrategy
from domain.models import OutcomeOutput, OutputStats
from domain.player import Player, Dealer
from application.blackjack.game import BlackJackGame
from application.blackjack.game_orchestrator import GameOrchestrator
from application.strategies.hit17_strategy import Hit17Strategy
from application.reporting.stats import StatCalculator
from application.reporting.report_generator import ReportGenerator

NUM_SHOES: Final = 10000
NUM_DECKS: Final = 6
STARTING_BANKROLL: Final = 1000
PLAYER_STRATEGY: BaseStrategy = Hit17Strategy()
BET_AMOUNT: Final = 25

def execute_sandbox() -> None:
    result_stats: list[OutputStats] = []
    for num in range(NUM_SHOES):
        if num % 1000 == 0:
            print(f"Processing shoe {num} of {NUM_SHOES}")
        player: Player = Player(STARTING_BANKROLL)
        dealer: Dealer = Dealer()
        game: BlackJackGame = BlackJackGame(player, dealer, num_decks=NUM_DECKS)
        orchestrator: GameOrchestrator = GameOrchestrator(game, PLAYER_STRATEGY)
        results: list[OutcomeOutput] = orchestrator.play_shoe(bet=BET_AMOUNT)
        hand_stats: OutputStats = StatCalculator.calculate_stats(results, STARTING_BANKROLL, player.bankroll)
        result_stats.append(hand_stats)

    stat_df = ReportGenerator.build_shoe_summary_df(result_stats)
    print(stat_df.head().to_string())