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
        self.player.buy(test_card)
        self.assertEqual(self.player.gold, 0)
        self.assertEqual(self.player.discard_pile[0].name, test_card)
        self.assertEqual(self.player.grimoire.library[test_card], 3)

if __name__ == '__main__':
    unittest.main()
