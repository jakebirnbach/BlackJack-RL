from domain.player import Player, Dealer
from application.blackjack.game import BlackJackGame
from application.blackjack.game_orchestrator import GameOrchestrator
from application.strategies.hit17_strategy import Hit17Strategy

def execute_sandbox():
    player = Player(1000)
    dealer = Dealer(100000)
    game = BlackJackGame(player, dealer, num_decks=6)
    orchestrator = GameOrchestrator(game, Hit17Strategy())

    results = orchestrator.play_shoe(bet=10)
    print(f"Hands played: {len(results)}")
    print(f"Results: {results}")
    print(f"Player bankroll: {player.bankroll}")
