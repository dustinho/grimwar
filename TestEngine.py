import unittest
from Player import *
from Board import *
from Unit import *
from Card import *
from Game import *

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.players = {}
        self.game.players[0] = Player(0)
        self.game.players[1] = Player(1)
        self.game.players[1].set_direction(Player.FACING_LEFT)
        self.game.board = Board(self.game, 3,7)

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

    def test_draw_and_play_card(self):
        self.game.players[0].deck.append(Card("Footman"))
        self.game.players[0].draw()
        self.game.play_card("Footman", 0, (0,0))
        self.assertEqual(self.game.board.grid[(0,0)].card.name, "Footman")
        self.assertEqual(self.game.players[0].gold, 7)

    def test_hero_death(self):
        live_hero_card = HeroCard('Arius')
        dead_hero_card = HeroCard('Arius')
        live_hero = Hero(live_hero_card, self.game.players[0])
        dead_hero = Hero(dead_hero_card, self.game.players[0])
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

