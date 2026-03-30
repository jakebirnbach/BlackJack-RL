import unittest
from src.domain.constants import Rank, Suit
from src.domain.models import Card
from src.domain.player import Player, Dealer


class TestPlayer(unittest.TestCase):

    def test_initial_bankroll(self):
        player = Player(100)
        self.assertEqual(player.bankroll, 100)

    def test_negative_bankroll_raises(self):
        with self.assertRaises(ValueError):
            Player(-10)

    def test_reset_hand(self):
        player = Player(100)
        player.hit(Card(Rank.FIVE, Suit.HEART))
        player.reset_hand()
        self.assertEqual(len(player.hand.cards), 0)
        self.assertEqual(player.hand.value, 0)

    def test_place_bet_deducts_bankroll(self):
        player = Player(100)
        bet = player.place_bet(25)
        self.assertEqual(bet, 25)
        self.assertEqual(player.bankroll, 75)

    def test_place_bet_exceeds_bankroll_raises(self):
        player = Player(100)
        with self.assertRaises(ValueError):
            player.place_bet(150)

    def test_place_bet_zero_raises(self):
        player = Player(100)
        with self.assertRaises(ValueError):
            player.place_bet(0)

    def test_place_bet_negative_raises(self):
        player = Player(100)
        with self.assertRaises(ValueError):
            player.place_bet(-5)

    def test_resolve_outcome(self):
        player = Player(100)
        player.place_bet(25)
        player.resolve_outcome(50)
        self.assertEqual(player.bankroll, 125)

    def test_hit_adds_card(self):
        player = Player(100)
        player.hit(Card(Rank.KING, Suit.SPADE))
        self.assertEqual(len(player.hand.cards), 1)
        self.assertEqual(player.hand.value, 10)

    def test_has_blackjack(self):
        player = Player(100)
        player.hit(Card(Rank.ACE, Suit.SPADE))
        player.hit(Card(Rank.KING, Suit.HEART))
        self.assertTrue(player.has_blackjack)

    def test_busted(self):
        player = Player(100)
        player.hit(Card(Rank.KING, Suit.SPADE))
        player.hit(Card(Rank.QUEEN, Suit.HEART))
        player.hit(Card(Rank.FIVE, Suit.DIAMOND))
        self.assertTrue(player.busted)

    def test_not_busted(self):
        player = Player(100)
        player.hit(Card(Rank.KING, Suit.SPADE))
        player.hit(Card(Rank.FIVE, Suit.HEART))
        self.assertFalse(player.busted)

    def test_buy_in(self):
        player = Player(100)
        player.buy_in(50)
        self.assertEqual(player.bankroll, 150)

    def test_buy_in_zero_raises(self):
        player = Player(100)
        with self.assertRaises(ValueError):
            player.buy_in(0)

    def test_buy_in_negative_raises(self):
        player = Player(100)
        with self.assertRaises(ValueError):
            player.buy_in(-10)


class TestDealer(unittest.TestCase):

    def test_inherits_player(self):
        dealer = Dealer(1000)
        self.assertIsInstance(dealer, Player)
        self.assertEqual(dealer.bankroll, 1000)

    def test_stand_on_17_default(self):
        dealer = Dealer(1000)
        self.assertTrue(dealer.stand_on_17)

    def test_stand_on_17_false(self):
        dealer = Dealer(1000, stand_on_17=False)
        self.assertFalse(dealer.stand_on_17)


if __name__ == "__main__":
    unittest.main()
