import unittest
from Player import *
from Card import *

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(0)

    def test_draw2_disc2(self):
        footman = Card.get_card('Footman')
        peasant = Card.get_card('Peasant')
        self.player.set_deck([footman, peasant])

        self.player.draw()
        self.player.draw()
        self.assertEqual(self.player.hand[0], footman)
        self.assertEqual(self.player.hand[1], peasant)

        self.player.discard(peasant)
        self.player.discard(footman)
        self.assertEqual(self.player.discard_pile[0], peasant)
        self.assertEqual(self.player.discard_pile[1], footman)

    def test_buy(self):
        test_card = "Footman"
        self.player.set_gold(Card.get_card(test_card).buy_cost)
        self.player.buy(test_card)
        self.assertEqual(self.player.gold, 0)
        self.assertEqual(self.player.discard_pile[0].name, test_card)
        self.assertEqual(self.player.grimoire.library[test_card], 3)

    def test_grimoire_properties(self):
        self.assertEqual(self.player.grimoire.cards["Footman"].name, "Footman")
        self.assertEqual(self.player.grimoire.cards["Peasant"].buy_cost, 25)

    def test_draw_and_recycle_deck(self):
        footman = Card.get_card('Footman')
        self.player.set_deck([footman])
        self.player.draw()
        self.player.discard(footman)
        self.assertEqual(self.player.discard_pile[0], footman)
        self.assertEqual(len(self.player.hand), 0)
        self.player.draw()
        self.assertEqual(self.player.hand[0], footman)


if __name__ == '__main__':
    unittest.main()
