import unittest
from Game import *
<<<<<<< HEAD
=======
from Unit import *
import logging
logging.getLogger().setLevel(logging.DEBUG)
>>>>>>> cb4f54b... Do move phase and damage things more correctly

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.players[0] = Player(0)
        self.game.players[1] = Player(1)
        self.game.players[1].set_direction(Player.FACING_LEFT)
        self.game.board = Board(self.game, field_length=7,field_width=3)

    def one_hero_kicking_ass(self):
        hero_card = HeroCard('Arius')
        hero = Hero(hero_card)
        self.game.players[0].inplay.append(hero_card)
        self.game.board.grid[(0,0)] = hero

        winner = self.game.main_loop()
        self.assertEquals(winner, 0)


