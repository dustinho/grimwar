import unittest
from Game import *
from Unit import *
import logging
logging.getLogger().setLevel(logging.DEBUG)


class TestGrimoire(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.board = Board(self.game, field_length=7, field_width=3)

    def test_buyable(self):
        """
        TODO(dho) Not done yet
        """
        p0 = self.game.players[0]
        p0.grimoire = Grimoire(p0, 'test_grimoire')
        names = p0.grimoire.get_buyable_card_names(p0)
        self.assertEquals(set(names), set(['Footman']))

        p0.gold = 9999
        p0.hand.append(Card.get_card('OneL T2'))
        self.game.play_building('OneL T2', 0, 0)
        self.game.pre_main_phases()

        names = p0.grimoire.get_buyable_card_names(p0)
        self.assertEquals(set(names), set(['Knight', 'Footman']))

        p0.grimoire.remove_from_grimoire('Knight')
        names = p0.grimoire.get_buyable_card_names(p0)
        self.assertEquals(set(names), set(['Footman']))

        p0.hand.append(Card.get_card('Mages T3'))
        self.game.play_building('Mages T3', 0, 1)
        self.game.pre_main_phases()
        names = p0.grimoire.get_buyable_card_names(p0)
        self.assertEquals(set(names), set(['Footman', 'Archmage']))











