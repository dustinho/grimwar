import unittest
from CardManager import CardManager

class TestCardManager(unittest.TestCase):
    def setUp(self):
      self.cm = CardManager()

    def test_draw2_disc2(self):
        self.cm.setDeck([1,2])

        self.cm.draw()
        self.cm.draw()
        self.assertEqual(self.cm.hand[0], 1)
        self.assertEqual(self.cm.hand[1], 2)

        self.cm.discardCard(1)
        self.cm.discardCard(2)
        self.assertEqual(self.cm.discard[0], 1)
        self.assertEqual(self.cm.discard[1], 2)

if __name__ == '__main__':
    unittest.main()
