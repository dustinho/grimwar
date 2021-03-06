import unittest
from Board import Board
from Card import *
from Player import *
from Unit import Unit
from Const import *
from Game import *
import logging
logging.getLogger().setLevel(logging.DEBUG)

TEST_FIELD_LENGTH = 9
TEST_FIELD_WIDTH = 3

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.b = Board(self.game, field_length=TEST_FIELD_LENGTH, field_width=TEST_FIELD_WIDTH)
        self.p1 = self.game.players[0]
        self.p2 = self.game.players[1]
        self.p2.set_direction(Const.FACING_LEFT)
        self.footman_card = Card.get_card("Footman")
        self.scout_card = Card.get_card("Scout")
        self.hero_card = HeroCard.get_card("Arius")
        self.worker_card = WorkerCard.get_card("Peasant")

    def test_place_footman_and_move_once(self):
        footman = Unit(self.footman_card, self.p1)
        self.b.grid[ (0,0) ] = footman
        self.b.do_movements(self.p1, self.p2)
        self.assertEqual(self.b.grid.pop( (1,0) ), footman)
        self.b.grid.clear()

    def test_moving_wont_go_past_edge(self):
        footman = Unit(self.footman_card, self.p1)
        footman._ammo = 0 #so footman doesn't attempt to damage player
        self.b.grid[ (TEST_FIELD_LENGTH-2,0) ] = footman
        self.b.do_movements(self.p1, self.p2)
        self.assertEqual(self.b.grid.pop( (TEST_FIELD_LENGTH-2,0) ), footman)
        self.b.grid.clear()

    def test_moving_wont_overtake(self):
        scout = Unit(self.scout_card, self.p1)
        footman = Unit(self.footman_card, self.p2)
        self.b.grid[(2,0)] = scout
        self.b.grid[(3,0)] = footman
        self.b.do_movements(self.p1, self.p2)
        self.assertEqual(self.b.grid[(2,0)], scout)
        self.assertEqual(self.b.grid[(3,0)], footman)
        self.b.grid.clear()

    def test_moving_slow_will_block_fast(self):
        scout = Unit(self.scout_card, self.p1)
        footman = Unit(self.footman_card, self.p1)
        self.b.grid[(2,0)] = scout
        self.b.grid[(3,0)] = footman
        self.b.do_movements(self.p1, self.p2)
        self.assertEqual(self.b.grid[(3,0)], scout)
        self.assertEqual(self.b.grid[(4,0)], footman)
        self.b.grid.clear()

    def test_attacking_should_do_damage(self):
        footman = Unit(self.footman_card, self.p1)
        footman2 = Unit(self.footman_card, self.p2)
        starthp = footman.get_curr_hp()
        starthp2 = footman.get_curr_hp()
        self.b.grid[(1,0)] = footman
        self.b.grid[(2,0)] = footman2
        self.b.do_all_attacks()
        self.assertEqual(footman.get_curr_hp() + footman2.get_damage(), starthp)
        self.assertEqual(footman2.get_curr_hp() + footman.get_damage(), starthp2)
        self.b.grid.clear()

    def test_place_unit(self):
        self.b.place_unit(self.footman_card, self.p1, (0,0))
        self.assertEqual(self.b.grid[(0,0)].card.name, "Footman")
        self.b.grid.clear()

if __name__ == "__main__":
    unittest.main()
