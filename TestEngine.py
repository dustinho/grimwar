import unittest
from Player import *
from Board import *
from Unit import *
from Card import *
from Game import *
from Const import *

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.players = {}
        self.game.players[0] = Player(0)
        self.game.players[1] = Player(1)
        self.game.players[1].set_direction(Const.FACING_LEFT)
        self.game.board = Board(self.game, 3,7)

    def test_cleanup_death(self):
        live_footman_card = Card.get_card('Footman')
        dead_footman_card = Card.get_card('Footman')
        live_footman = Unit.get_unit(live_footman_card, self.game.players[0])
        dead_footman = Unit.get_unit(dead_footman_card, self.game.players[0])
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
        """
        This is way too rigid while we're still messing with worker gold
        amounts.
        Reimplement when we're more sure of what amounts we're going with


        self.game.board = Board(self.game, 19,5)
        peasant_card = Card.get_card("Peasant")
        peasant = Unit.get_unit(peasant_card, self.game.players[0])
        self.game.players[0].inplay.append(peasant_card)
        self.game.board.grid[(0,0)] = peasant
        self.assertEqual(self.game.players[0].gold,10)
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.assertEqual(self.game.players[0].gold,15)
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.assertEqual(self.game.board.grid[(6,0)], peasant)
        self.assertEqual(self.game.players[0].gold,20)
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.assertEqual(self.game.board.grid[(10,0)], peasant)
        self.assertEqual(self.game.players[0].gold,27)
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.assertEqual(self.game.board.grid[(13,0)], peasant)
        self.assertEqual(self.game.players[0].gold,33)
        """

    def test_draw_and_play_card(self):
        self.game.players[0].deck.append(Card.get_card("Footman"))
        self.game.players[0].draw()
        self.game.play_unit("Footman", 0, (0,0))
        self.assertEqual(self.game.board.grid[(0,0)].card.name, "Footman")
        #self.assertEqual(self.game.players[0].gold, 7)

    def test_hero_death(self):
        live_hero_card = Card.get_card('Arius')
        dead_hero_card = Card.get_card('Arius')
        live_hero = Unit.get_unit(live_hero_card, self.game.players[0])
        dead_hero = Unit.get_unit(dead_hero_card, self.game.players[0])
        self.game.players[0].inplay.append(live_hero_card)
        self.game.players[0].inplay.append(dead_hero_card)
        dead_hero._hp = 0

        self.game.board.grid[(3,3)] = live_hero
        self.game.board.grid[(4,4)] = dead_hero

        self.game.cleanup_phase()
        self.assertTrue((3,3) in self.game.board.grid)
        self.assertFalse((4,4) in self.game.board.grid)
        self.assertEqual(len(self.game.players[0].discard_pile), 0)
        self.assertEqual(len(self.game.players[0].deck), 1)
        self.assertEqual(len(self.game.players[0].inplay), 1)

if __name__ == "__main__":
    unittest.main()

