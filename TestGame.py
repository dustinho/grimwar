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
        self.game.players[0].gold += draw_card.cost
        self.game.play_spell('Draw', 0, 0)
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

    def test_heal_row(self):
        """
        Tests that the heal_row spell heals correctly after cast_time turns
        """
        footman_card1 = Card.get_card('Footman')
        footman1 = Unit.get_unit(footman_card1, self.game.players[0])
        self.game.players[0].inplay.append(footman_card1)
        self.game.board.grid[(4,0)] = footman1
        footman_card2 = Card.get_card('Footman')
        footman2 = Unit.get_unit(footman_card2, self.game.players[0])
        self.game.players[0].inplay.append(footman_card2)
        self.game.board.grid[(1,1)] = footman2
        footman_card3 = Card.get_card('Footman')
        footman3 = Unit.get_unit(footman_card3, self.game.players[1])
        self.game.players[1].inplay.append(footman_card3)
        self.game.board.grid[(3,0)] = footman3
        heal_row = Card.get_card('Heal Row')
        self.game.players[0].hand.append(heal_row)
        self.game.players[0].gold += heal_row.cost
        self.game.play_spell('heal row', 0, 0)
        footmen = [footman1, footman2, footman3]
        footmen_health = [unit.get_curr_hp() for unit in footmen]
        self.assertEquals(footmen_health, [15, 15, 15])
        for footman in footmen:
            footman.take_damage(3)
        footmen_health = [unit.get_curr_hp() for unit in [footman1, footman2, footman3]]
        self.assertEquals(footmen_health, [12, 12, 12])
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.game.main_loop_once()
        self.game.main_loop_once()
        footmen_health = [unit.get_curr_hp() for unit in [footman1, footman2, footman3]]
        self.assertEquals(footmen_health, [15, 12, 12])

    def test_econ_build(self):
        """
        Tests that having the econ building will upgrade peasants correctly.
        """
        self.game.players[0].gold = 9999

        discard = self.game.players[0].discard_pile
        discard.append(Card.get_card('Peasant'))
        discard.append(Card.get_card('Peasant'))
        self.assertEquals(len(discard), 2)

        self.game.players[0].hand.append(Card.get_card('Econ'))
        self.game.play_building('Econ', 0, 0)
        self.game.main_loop_once()

        discard = self.game.players[0].discard_pile
        n_peasants = len([x for x in discard if x.name == 'Peasant'])
        n_speasants = len([x for x in discard if x.name == 'SPeasant'])

        self.assertEquals(n_peasants, 0)
        self.assertEquals(n_speasants, 2)







