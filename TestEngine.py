import unittest
from Player import *
from Board import *
from Unit import *
from Card import *
from WorkerCard import *
from HeroCard import *
from Game import *

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.players = {}
        self.game.players[0] = Player()
        self.game.players[1] = Player()
        self.game.players[1].set_direction(Player.FACING_LEFT)
        self.game.board = Board(3,7)

    def test_cleanup_death(self):
        live_footman_card = Card('Footman')
        dead_footman_card = Card('Footman')
        live_footman = Unit(live_footman_card, self.game.players[0])
        dead_footman = Unit(dead_footman_card, self.game.players[0])
        self.game.players[0].inplay.append(live_footman_card)
        self.game.players[0].inplay.append(dead_footman_card)
        dead_footman._hp = 0

        self.game.board.grid[(1,1)] = live_footman
        self.game.board.grid[(2,2)] = dead_footman

        self.game.cleanup_phase()
        self.assertTrue((1,1) in self.game.board.grid)
        self.assertFalse((2,2) in self.game.board.grid)
        self.assertEqual(len(self.game.players[0].discard_pile), 1)
        self.assertEqual(len(self.game.players[0].inplay), 1)

    def test_worker_money(self):
        # TODO
        self.assertEqual(1,1)

if __name__ == "__main__":
    unittest.main()

