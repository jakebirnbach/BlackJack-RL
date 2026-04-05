from domain.models import OutcomeOutput
from domain.player import Player, Dealer
from application.blackjack.game import BlackJackGame
from application.blackjack.game_orchestrator import GameOrchestrator
from application.strategies.hit17_strategy import Hit17Strategy
from application.reporting.stats import StatCalculator

def execute_sandbox():
    starting_bankroll = 1000
    player: Player = Player(starting_bankroll)
    dealer: Dealer = Dealer(100000)
    game: BlackJackGame = BlackJackGame(player, dealer, num_decks=6)
    orchestrator: GameOrchestrator = GameOrchestrator(game, Hit17Strategy())

    results: list[OutcomeOutput] = orchestrator.play_shoe(bet=15)
    ending_bankroll = player.bankroll
    hand_stats = StatCalculator.calculate_stats(results, starting_bankroll, ending_bankroll)
    print(hand_stats)
