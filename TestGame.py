import unittest
from Game import *
from Unit import *
import logging
logging.getLogger().setLevel(logging.DEBUG)

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.board = Board(self.game, field_length=7,field_width=3)

    def test_one_hero_kicking_ass(self):
        hero_card = Card.get_card('Arius')
        hero = Hero(hero_card, self.game.players[0])
        self.game.players[0].inplay.append(hero_card)
        self.game.board.grid[(0,0)] = hero

        winner = self.game.main_loop()
        self.assertEquals(winner, 0)

    def test_cast_draw(self):
        """
        Tests that draw 3 spell correctly draws after cast_time turns
        """
        draw_card = Card.get_card('Draw')
        self.game.players[0].hand.append(draw_card)
        self.game.play_spell('draw', 0, 0)
        cards_in_hand = len(self.game.players[0].hand)
        cast_time = draw_card.cast_time
        for x in reversed(range(cast_time)):
            self.game.main_loop_once()
            print x, self.game.board.spells[0][0]
            if x != 0:
                self.assertEquals(
                    len(self.game.players[0].hand), cards_in_hand)
            else:
                self.assertEquals(
                    len(self.game.players[0].hand), cards_in_hand+3)


