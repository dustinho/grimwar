import unittest
from Game import *
from Unit import *
import logging
logging.getLogger().setLevel(logging.DEBUG)

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.board = Board(self.game, field_length=7,field_width=3)

    def test_one_hero_kicking_ass(self):
        hero_card = Card.get_card('Arius')
        hero = Hero(hero_card, self.game.players[0])
        self.game.players[0].inplay.append(hero_card)
        self.game.board.grid[(0,0)] = hero

        winner = self.game.main_loop()
        self.assertEquals(winner, 0)


