import unittest
from Player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(0)

    def test_draw2_disc2(self):
        self.player.set_deck([1,2])

        self.player.draw()
        self.player.draw()
        self.assertEqual(self.player.hand[0], 1)
        self.assertEqual(self.player.hand[1], 2)

        self.player.discard(1)
        self.player.discard(2)
        self.assertEqual(self.player.discard_pile[0], 1)
        self.assertEqual(self.player.discard_pile[1], 2)

    def test_buy(self):
        test_card = "Footman"
        self.player.buy(test_card)
        self.assertEqual(self.player.gold, 0)
        self.assertEqual(self.player.discard_pile[0], test_card)
        self.assertEqual(self.player.grimoire.library[test_card], 3)

if __name__ == '__main__':
    unittest.main()
