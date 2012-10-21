import unittest
from Player import *
from Board import *
from Unit import *
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




if __name__ == "__main__":
    unittest.main()

