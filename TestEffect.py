import unittest
from Game import *
from Unit import *
from Effect import *
import logging
logging.getLogger().setLevel(logging.DEBUG)

class TestEffect(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.board = Board(self.game, field_length=7,field_width=3)

    def test_draw(self):
        self.game.players[0].hand = deque()
        cards_in_hand = len(self.game.players[0].hand)
        Effect.applyEffect(
            "draw",
            self.game.players[0],
            self.game.players[1],
            None,
            self.game.board,
            [3]
        )
        self.assertEquals(len(self.game.players[0].hand), cards_in_hand+3)


