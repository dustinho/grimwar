import unittest
from Player import *
from Board import *
from Unit import *
from Card import *
from gw import cleanup_phase

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.players = {}
        self.players[0] = Player()
        self.players[1] = Player()
        self.board = Board(3,7)

    def test_cleanup_death(self):
        live_footman_card = Card('Footman')
        dead_footman_card = Card('Footman')
        live_footman = Unit(live_footman_card, self.players[0])
        dead_footman = Unit(dead_footman_card, self.players[0])
        self.players[0].inplay.append(live_footman_card)
        self.players[0].inplay.append(dead_footman_card)
        dead_footman._hp = 0

        self.board.grid[(1,1)] = live_footman
        self.board.grid[(2,2)] = dead_footman

        cleanup_phase(self.players, self.board)
        self.assertTrue((1,1) in self.board.grid)
        self.assertFalse((2,2) in self.board.grid)
        self.assertEqual(len(self.players[0].hand), 1)
        self.assertEqual(len(self.players[0].inplay), 1)

    def test_money_phase(self):
        worker_0 = Unit(Card('Peon'))
        worker_2 = Unit(Card('Peon'))
        sector2_col = board.SECTORS[2]

        self.board.grid[(1,0)] = worker_0
        self.board.grid[(sector2_col,0)] = worker_2

if __name__ == "__main__":
    unittest.main()

