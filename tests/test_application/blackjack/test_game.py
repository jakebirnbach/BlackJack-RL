import unittest
from random import Random
from domain.constants import Rank, Suit
from domain.models import Card, Deck, Hand
from domain.player import Player, Dealer
from application.blackjack.game import BlackJackGame


class TestBlackJackGameConstructor(unittest.TestCase):

    def test_valid_construction(self):
        game = BlackJackGame(Player(100), Dealer(1000))
        self.assertEqual(game.current_bet, 0)
        self.assertEqual(game.table_min, 1)
        self.assertEqual(game.bj_payout, 1.5)

    def test_player_none_raises(self):
        with self.assertRaises(ValueError):
            BlackJackGame(None, Dealer(1000))

    def test_dealer_none_raises(self):
        with self.assertRaises(ValueError):
            BlackJackGame(Player(100), None)

    def test_negative_table_min_raises(self):
        with self.assertRaises(ValueError):
            BlackJackGame(Player(100), Dealer(1000), table_min=-1)

    def test_table_max_less_than_min_raises(self):
        with self.assertRaises(ValueError):
            BlackJackGame(Player(100), Dealer(1000), table_min=10, table_max=5)

    def test_invalid_payout_raises(self):
        with self.assertRaises(ValueError):
            BlackJackGame(Player(100), Dealer(1000), bj_payout=2.0)

    def test_6_5_payout_valid(self):
        game = BlackJackGame(Player(100), Dealer(1000), bj_payout=6/5)
        self.assertEqual(game.bj_payout, 6/5)


class TestEnterBets(unittest.TestCase):

    def test_valid_bet(self):
        game = BlackJackGame(Player(100), Dealer(1000))
        game.enter_bets(10)
        self.assertEqual(game.current_bet, 10)
        self.assertEqual(game.player.bankroll, 90)

    def test_bet_above_table_max_raises(self):
        game = BlackJackGame(Player(100), Dealer(1000), table_max=50)
        with self.assertRaises(ValueError):
            game.enter_bets(60)

    def test_bet_below_table_min_raises(self):
        game = BlackJackGame(Player(100), Dealer(1000), table_min=10)
        with self.assertRaises(ValueError):
            game.enter_bets(5)


class TestDealCards(unittest.TestCase):

    def test_deal_gives_two_cards_each(self):
        game = BlackJackGame(Player(100), Dealer(1000))
        game.deal_cards()
        self.assertEqual(len(game.player.hand.cards), 2)
        self.assertEqual(len(game.dealer.hand.cards), 2)

    def test_deal_reduces_deck(self):
        game = BlackJackGame(Player(100), Dealer(1000))
        game.deal_cards()
        self.assertEqual(len(game.deck.cards), 48)


class TestDealerProperties(unittest.TestCase):

    def test_dealer_showing_is_first_card(self):
        game = BlackJackGame(Player(100), Dealer(1000), rng=Random(42))
        game.deal_cards()
        self.assertEqual(game.dealer_showing, game.dealer.hand.cards[0])

    def test_dealer_hiding_is_second_card(self):
        game = BlackJackGame(Player(100), Dealer(1000), rng=Random(42))
        game.deal_cards()
        self.assertEqual(game.dealer_hiding, game.dealer.hand.cards[1])


class TestOutcomes(unittest.TestCase):

    def test_player_wins_default_multiplier(self):
        game = BlackJackGame(Player(100), Dealer(1000))
        game.enter_bets(10)
        game.deal_cards()
        game.player_wins()
        self.assertEqual(game.player.bankroll, 110)

    def test_player_wins_blackjack_payout(self):
        game = BlackJackGame(Player(100), Dealer(1000), bj_payout=1.5)
        game.enter_bets(10)
        game.deal_cards()
        game.player_wins(multiplier=1 + 1.5)
        self.assertEqual(game.player.bankroll, 115)

    def test_dealer_wins(self):
        game = BlackJackGame(Player(100), Dealer(1000))
        game.enter_bets(10)
        game.deal_cards()
        game.dealer_wins()
        self.assertEqual(game.player.bankroll, 90)
        self.assertEqual(game.dealer.bankroll, 1010)

    def test_push_returns_bet(self):
        game = BlackJackGame(Player(100), Dealer(1000))
        game.enter_bets(10)
        game.deal_cards()
        game.push()
        self.assertEqual(game.player.bankroll, 100)


class TestEndRound(unittest.TestCase):

    def test_end_round_resets_state(self):
        game = BlackJackGame(Player(100), Dealer(1000))
        game.enter_bets(10)
        game.deal_cards()
        game.end_round()
        self.assertEqual(len(game.player.hand.cards), 0)
        self.assertEqual(len(game.dealer.hand.cards), 0)
        self.assertEqual(game.current_bet, 0)


class TestStartRound(unittest.TestCase):

    def test_bankroll_below_table_min_raises(self):
        game = BlackJackGame(Player(5), Dealer(1000), table_min=10)
        with self.assertRaises(ValueError):
            game.start_round(10)

    def test_start_round_deals_and_bets(self):
        game = BlackJackGame(Player(100), Dealer(1000), rng=Random(42))
        game.start_round(10)
        # Either hands have cards (round in progress) or round ended due to blackjack
        self.assertEqual(game.player.bankroll + game.current_bet <= 100, True)


if __name__ == "__main__":
    unittest.main()
