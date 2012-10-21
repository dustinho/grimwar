import unittest
from Board import Board
from Card import Card
from Player import *
from Unit import Unit

TEST_FIELD_LENGTH = 9
TEST_FIELD_WIDTH = 3

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.b = Board(field_length=TEST_FIELD_LENGTH, field_width=TEST_FIELD_WIDTH)
        self.p = Player()
        self.footman_card = Card("Footman")

    def test_place_footman_and_move_once(self):
        footman = Unit(self.footman_card, self.p)
        self.b.grid[ (0,0) ] = footman
        self.b.do_all_movements(self.p)
        self.assertEqual(self.b.grid.pop( (1,0) ), footman)

    def test_moving_wont_go_past_edge(self):
        footman = Unit(self.footman_card, self.p)
        self.b.grid[ (TEST_FIELD_LENGTH,0) ] = footman
        self.b.do_all_movements(self.p)
        self.assertEqual(self.b.grid.pop( (TEST_FIELD_LENGTH,0) ), footman)

if __name__ == "__main__":
    unittest.main()
