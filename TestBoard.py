import unittest
from Board import Board
from Card import Card
from HeroCard import HeroCard
from WorkerCard import WorkerCard
from Player import *
from Unit import Unit

TEST_FIELD_LENGTH = 9
TEST_FIELD_WIDTH = 3

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.b = Board(field_length=TEST_FIELD_LENGTH, field_width=TEST_FIELD_WIDTH)
        self.p1 = Player()
        self.p2 = Player()
        self.p2.set_direction(Player.FACING_LEFT)
        self.footman_card = Card("Footman")
        self.fast_footman_card = Card("Footman")
        self.fast_footman_card.speed = 2
        self.hero_card = HeroCard("Arius")
        self.worker_card = WorkerCard("Peon")

    def test_place_footman_and_move_once(self):
        footman = Unit(self.footman_card, self.p1)
        self.b.grid[ (0,0) ] = footman
        self.b.do_all_movements(self.p1)
        # N.B. a movement speed of 1 means you move two columns per turn, due
        # to the way we number the grid.  What fun!
        self.assertEqual(self.b.grid.pop( (2,0) ), footman)

    def test_moving_wont_go_past_edge(self):
        footman = Unit(self.footman_card, self.p1)
        self.b.grid[ (TEST_FIELD_LENGTH-3,0) ] = footman
        self.b.do_all_movements(self.p1)
        self.assertEqual(self.b.grid.pop( (TEST_FIELD_LENGTH-3,0) ), footman)

    def test_moving_wont_overtake(self):
        fast_footman = Unit(self.fast_footman_card, self.p1)
        footman = Unit(self.footman_card, self.p2)
        self.b.grid[(2,0)] = fast_footman
        self.b.grid[(4,0)] = footman
        self.b.do_all_movements(self.p1)
        self.assertEqual(self.b.grid[(2,0)], fast_footman)
        self.b.do_all_movements(self.p2)
        self.assertEqual(self.b.grid[(4,0)], footman)
        self.b.grid.clear()

    def test_moving_slow_will_block_fast(self):
        fast_footman = Unit(self.fast_footman_card, self.p1)
        footman = Unit(self.footman_card, self.p1)
        self.b.grid[(2,0)] = fast_footman
        self.b.grid[(4,0)] = footman
        self.b.do_all_movements(self.p1)
        self.assertEqual(self.b.grid[(4,0)], fast_footman)
        self.assertEqual(self.b.grid[(6,0)], footman)
        self.b.grid.clear()

if __name__ == "__main__":
    unittest.main()
