import unittest
from Game import *
from Unit import *
import logging
logging.getLogger().setLevel(logging.DEBUG)

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.board = Board(self.game, field_length=7,field_width=3)

        self.footman_card = Card.get_card("Footman")
        self.rifleman_card = Card.get_card("Rifleman")
        self.scout_card = Card.get_card("Scout")
        self.hero_card = HeroCard.get_card("Arius")
        self.worker_card = WorkerCard.get_card("Peasant")

        self.p0 = self.game.players[0]
        self.p1 = self.game.players[1]
        self.b = self.game.board
        self.g = self.game

    def test_one_hero_kicking_ass(self):
        self.b.place_unit(self.hero_card, self.p0, (0,0))

        winner = self.g.main_loop()
        self.assertEquals(winner, 0)

    def test_cast_draw(self):
        """
        Tests that draw 3 spell correctly draws after cast_time turns
        """
        draw_card = Card.get_card('Draw')
        self.p0.hand.append(draw_card)
        self.p0.gold += draw_card.cost
        self.g.play_spell('Draw', 0, 0)
        cards_in_hand = len(self.p0.hand)
        cast_time = draw_card.cast_time
        for x in reversed(range(cast_time)):
            self.g.main_loop_once()
            print x, self.b.spells[0][0]
            if x != 0:
                self.assertEquals(
                    len(self.p0.hand), cards_in_hand)
            else:
                self.assertEquals(
                    len(self.p0.hand), cards_in_hand+3)

    def test_heal_row(self):
        """
        Tests that the heal_row spell heals correctly after cast_time turns
        """
        self.b.place_unit(self.footman_card, self.p0, (4,0))
        self.b.place_unit(self.footman_card, self.p0, (1,1))
        self.b.place_unit(self.footman_card, self.p0, (3,0))
        self.b.place_unit(self.footman_card, self.p1, (2,0))

        heal_row = Card.get_card('Heal Row')
        self.p0.hand.append(heal_row)
        self.p0.gold += heal_row.cost
        self.g.play_spell('Heal Row', 0, 0)
        cast_time = heal_row.cast_time

        footmen = [self.b.grid[(4,0)], self.b.grid[(1,1)],
                self.b.grid[(3,0)], self.b.grid[(2,0)]]
        footmen_health = [unit.get_curr_hp() for unit in footmen]
        self.assertEquals(footmen_health, [15, 15, 15, 15])

        for footman in footmen:
            footman.take_damage(3)

        for x in reversed(range(cast_time)):
            self.g.main_loop_once()
            if x != 0:
                footmen_health = [unit.get_curr_hp() for unit in footmen]
                self.assertEquals(footmen_health, [12, 12, 12, 12])
            else:
                footmen_health = [unit.get_curr_hp() for unit in footmen]
                self.assertEquals(footmen_health, [15, 12, 15, 12])

    def test_econ_build(self):
        """
        Tests that having the econ building will upgrade peasants correctly.
        """
        self.p0.gold = 9999

        discard = self.p0.discard_pile
        discard.append(Card.get_card('Peasant'))
        discard.append(Card.get_card('Peasant'))
        self.assertEquals(len(discard), 2)

        self.p0.hand.append(Card.get_card('Econ'))
        self.g.play_building('Econ', 0, 0)
        self.g.main_loop_once()

        discard = self.p0.discard_pile
        n_peasants = len([x for x in discard if x.name == 'Peasant'])
        n_speasants = len([x for x in discard if x.name == 'SPeasant'])

        self.assertEquals(n_peasants, 0)
        self.assertEquals(n_speasants, 2)

    def test_buff_row(self):
        self.p0.gold = 9999
        self.p0.hand.append(Card.get_card('Buff Row'))

        footman1 = self.b.place_unit(self.footman_card, self.p0, (4,0))

        self.assertEquals(footman1.get_damage(), 5)
        self.g.play_spell('Buff Row', 0, 0)

        self.g.main_loop_once()
        self.g.main_loop_once()

        # Spell should take effect on the third turn after play
        self.assertEquals(footman1.get_damage(), 5)
        self.g.main_loop_once()
        self.assertEquals(footman1.get_damage(), 6)

        # Modifier should last a total of 3 turns
        self.g.main_loop_once()
        self.assertEquals(footman1.get_damage(), 6)
        self.g.main_loop_once()
        # At the end of the third turn, the unit reverts back to 5 attack.
        self.g.pre_main_phases()
        self.assertEquals(footman1.get_damage(), 5)

    def test_two_footmen(self):
        footman1 = self.b.place_unit(self.footman_card, self.p0, (2,1))
        footman2 = self.b.place_unit(self.footman_card, self.p1, (4,1))

        footmen = [footman1, footman2]
        footmen_health = [unit.get_curr_hp() for unit in footmen]
        self.assertEquals(footmen_health, [15, 15])
        for x in xrange(5):
            self.g.main_loop_once()

        #footmen_health = [unit.get_curr_hp() for unit in footmen]
        #self.assertEquals(footmen_health, [0, 0])


    def test_arius_two_footman_1(self):
        arius = self.b.place_unit(self.hero_card, self.p0, (3,1))
        footman1 = self.b.place_unit(self.footman_card, self.p1, (4,2))
        footman2 = self.b.place_unit(self.footman_card, self.p1, (5,2))

        units = [arius, footman1, footman2]
        unit_health = [unit.get_curr_hp() for unit in units]
        self.assertEquals(unit_health, [30, 15, 15])

        for x in xrange(4):
            self.g.main_loop_once()
        
        unit_health = [unit.get_curr_hp() for unit in units]
        self.assertEquals(unit_health, [30, 10, 10])

    def test_two_riflemen_two_footmen(self):
        footman1 = self.b.place_unit(self.footman_card, self.p0, (0,0))
        footman2 = self.b.place_unit(self.footman_card, self.p0, (1,0))
        rifleman1 = self.b.place_unit(self.rifleman_card, self.p1, (5, 0))
        rifleman2 = self.b.place_unit(self.rifleman_card, self.p1, (6, 0))

        units = [footman1, footman2, rifleman1, rifleman2]
        unit_health = [unit.get_curr_hp() for unit in units]
        self.assertEquals(unit_health, [15, 15, 10, 10])

        for x in xrange(10):
            self.g.main_loop_once()

        unit_health = [unit.get_curr_hp() for unit in units]
        self.assertEquals(unit_health, [-1, -5, 0, 5])

    def test_two_riflemen_two_scouts(self):
        rifleman1 = self.b.place_unit(self.rifleman_card, self.p0, (0, 0))
        rifleman2 = self.b.place_unit(self.rifleman_card, self.p0, (1, 0))
        scout1 = self.b.place_unit(self.scout_card, self.p1, (5, 0))
        scout2 = self.b.place_unit(self.scout_card, self.p1, (6, 0))
        
        units = [rifleman1, rifleman2, scout1, scout2]
        unit_health = [unit.get_curr_hp() for unit in units]
        self.assertEquals(unit_health, [10, 10, 10, 10])

        for x in xrange(10):
            self.g.main_loop_once()

        unit_health = [unit.get_curr_hp() for unit in units]
        self.assertEquals(unit_health, [10, 0, -2, -6])
        


if __name__ == "__main__":
    unittest.main()

