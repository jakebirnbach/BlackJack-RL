import unittest
from random import Random
from domain.constants import Suit, Rank
from domain.models import Card, Deck, Hand


class TestCard(unittest.TestCase):

    def test_number_card_points(self):
        card = Card(Rank.FIVE, Suit.HEART)
        self.assertEqual(card.rank.points, 5)

    def test_face_card_points(self):
        self.assertEqual(Card(Rank.JACK, Suit.SPADE).rank.points, 10)
        self.assertEqual(Card(Rank.QUEEN, Suit.DIAMOND).rank.points, 10)
        self.assertEqual(Card(Rank.KING, Suit.CLUB).rank.points, 10)

    def test_ace_points(self):
        card = Card(Rank.ACE, Suit.HEART)
        self.assertEqual(card.rank.points, 11)

    def test_str(self):
        card = Card(Rank.ACE, Suit.SPADE)
        self.assertEqual(str(card), "Ace of Spade")


class TestDeck(unittest.TestCase):

    def test_deck_has_52_cards(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deal_returns_card_and_reduces_size(self):
        deck = Deck()
        card = deck.deal()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), 51)

    def test_deal_empty_deck_raises(self):
        deck = Deck()
        for _ in range(52):
            deck.deal()
        with self.assertRaises(ValueError):
            deck.deal()

    def test_reset_restores_deck(self):
        deck = Deck()
        for _ in range(10):
            deck.deal()
        deck.reset()
        self.assertEqual(len(deck.cards), 52)

    def test_seeded_rng_produces_same_order(self):
        deck1 = Deck(rng=Random(42))
        deck2 = Deck(rng=Random(42))
        for _ in range(10):
            c1 = deck1.deal()
            c2 = deck2.deal()
            self.assertEqual(c1.rank, c2.rank)
            self.assertEqual(c1.suit, c2.suit)


class TestHand(unittest.TestCase):

    def test_basic_value(self):
        hand = Hand()
        hand.add_card(Card(Rank.FIVE, Suit.HEART))
        hand.add_card(Card(Rank.THREE, Suit.CLUB))
        self.assertEqual(hand.value, 8)

    def test_soft_hand_with_ace(self):
        hand = Hand()
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.SIX, Suit.HEART))
        self.assertEqual(hand.value, 17)
        self.assertTrue(hand.is_soft)

    def test_ace_downgrades_to_avoid_bust(self):
        hand = Hand()
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.SIX, Suit.HEART))
        hand.add_card(Card(Rank.KING, Suit.DIAMOND))
        self.assertEqual(hand.value, 17)
        self.assertFalse(hand.is_soft)

    def test_two_aces(self):
        hand = Hand()
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.ACE, Suit.HEART))
        self.assertEqual(hand.value, 12)

    def test_is_blackjack(self):
        hand = Hand()
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.KING, Suit.HEART))
        self.assertTrue(hand.is_blackjack)

    def test_three_cards_totaling_21_not_blackjack(self):
        hand = Hand()
        hand.add_card(Card(Rank.SEVEN, Suit.SPADE))
        hand.add_card(Card(Rank.SEVEN, Suit.HEART))
        hand.add_card(Card(Rank.SEVEN, Suit.DIAMOND))
        self.assertEqual(hand.value, 21)
        self.assertFalse(hand.is_blackjack)

    def test_is_bust(self):
        hand = Hand()
        hand.add_card(Card(Rank.KING, Suit.SPADE))
        hand.add_card(Card(Rank.QUEEN, Suit.HEART))
        hand.add_card(Card(Rank.FIVE, Suit.DIAMOND))
        self.assertTrue(hand.is_bust)

    def test_not_bust(self):
        hand = Hand()
        hand.add_card(Card(Rank.KING, Suit.SPADE))
        hand.add_card(Card(Rank.QUEEN, Suit.HEART))
        self.assertFalse(hand.is_bust)

    def test_str(self):
        hand = Hand()
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.KING, Suit.HEART))
        self.assertEqual(str(hand), "[Ace of Spade, King of Heart] (value: 21)")


if __name__ == "__main__":
    unittest.main()
