import unittest
from Game import *
from Unit import *
import logging
logging.getLogger().setLevel(logging.DEBUG)

class TestGrimoire(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.board = Board(self.game, field_length=7,field_width=3)

    def test_buyable(self):
        """
        TODO(dho) Not done yet
        """
        self.game.players[0].gold = 9999
        self.game.players[0].hand.append(Card.get_card('OneL T2'))
        self.game.play_building('OneL T2', 0, 0)
        self.game.pre_main_phases()












