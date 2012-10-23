import unittest
from Game import *

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.players[0] = Player()
        self.game.players[1] = Player()
        self.game.players[1].set_direction(Player.FACING_LEFT)
        self.game.board = Board(3,7)

    def one_hero_kicking_ass(self):
        hero_card = HeroCard('Arius')
        hero = Hero(hero_card)
        self.game.players[0].inplay.append(hero_card)
        self.game.board.grid[(0,0)] = hero

        winner = self.game.main_loop()
        self.assertEquals(winner, 0)


