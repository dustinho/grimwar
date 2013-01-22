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
        self.trebuchet_card = Card.get_card("Trebuchet")

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
        self.p0.hand = deque()
        draw_card = Card.get_card('Draw')
        self.p0.hand.append(draw_card)
        self.p0.gold += draw_card.cost
        self.g.play_spell('Draw', 0, 0)
        cast_time = draw_card.cast_time
        cards_in_hand = len(self.p0.hand)

        for x in reversed(range(cast_time)):
            self.g.main_loop_once()
            print x, self.b.spells[0][0]
            if x != 0:
                cards_in_hand = len(self.p0.hand)
            else:
                self.assertEquals(
                    len(self.p0.hand),
                    min(cards_in_hand + 3, self.p0.MAX_HAND_SIZE)
                    )

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

        footman1 = self.b.place_unit(self.footman_card, self.p0, (1,0))

        self.assertEquals(footman1.get_damage(), 5)
        self.assertEquals(footman1.get_curr_ammo(), 5)
        self.assertEquals(footman1.get_curr_hp(), 15)
        self.assertEquals(footman1.get_speed(),1)
        self.g.play_spell('Buff Row', 0, 0)

        self.g.main_loop_once()
        self.g.main_loop_once()

        # Spell should take effect on the third turn after play
        self.assertEquals(footman1.get_damage(), 5)
        self.assertEquals(footman1.get_curr_ammo(), 5)
        self.assertEquals(footman1.get_curr_hp(), 15)
        self.assertEquals(footman1.get_speed(),1)
        self.g.main_loop_once()
        self.assertEquals(footman1.get_damage(), 6)
        self.assertEquals(footman1.get_curr_ammo(), 5)
        self.assertEquals(footman1.get_curr_hp(), 15)
        self.assertEquals(footman1.get_speed(),1)

        # Modifier should last a total of 3 turns
        self.g.main_loop_once()
        self.assertEquals(footman1.get_damage(), 6)
        self.g.main_loop_once()
        # At the end of the third turn, the unit reverts back to 5 attack.
        self.g.pre_main_phases()
        self.assertEquals(footman1.get_damage(), 5)

    def test_test_buff_row(self):
        self.p0.gold = 9999
        self.p0.hand.append(Card.get_card('Test Buff Row'))

        footman1 = self.b.place_unit(self.footman_card, self.p0, (1,0))

        self.assertEquals(footman1.get_damage(), 5)
        self.assertEquals(footman1.get_curr_ammo(), 5)
        self.assertEquals(footman1.get_curr_hp(), 15)
        self.assertEquals(footman1.get_speed(),1)
        self.g.play_spell('Test Buff Row', 0, 0)

        self.g.main_loop_once()
        self.g.main_loop_once()

        # Spell should take effect on the third turn after play
        self.assertEquals(footman1.get_damage(), 5)
        self.assertEquals(footman1.get_curr_ammo(), 5)
        self.assertEquals(footman1.get_curr_hp(), 15)
        self.assertEquals(footman1.get_speed(),1)
        self.g.main_loop_once()
        self.assertEquals(footman1.get_damage(), 6)
        self.assertEquals(footman1.get_curr_ammo(), 6)
        self.assertEquals(footman1.get_curr_hp(), 20)
        self.assertEquals(footman1.get_speed(),2)

        # Modifier should last a total of 3 turns
        self.g.main_loop_once()
        self.assertEquals(footman1.get_damage(), 6)
        self.assertEquals(footman1.get_curr_ammo(), 5) #attacks
        self.assertEquals(footman1.get_curr_hp(), 20)
        self.assertEquals(footman1.get_speed(),2)
        self.g.main_loop_once()
        # At the end of the third turn, the unit reverts back to 5 attack.
        self.g.pre_main_phases()
        self.assertEquals(footman1.get_damage(), 5)
        self.assertEquals(footman1.get_curr_ammo(), 3) #attacks
        self.assertEquals(footman1.get_curr_hp(), 15)
        self.assertEquals(footman1.get_speed(),1)


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
        
    def test_ragnarok(self):
        ragnarok = Card.get_card('Ragnarok')
        self.p0.hand.append(ragnarok)
        self.p0.gold += ragnarok.cost
        self.g.play_spell('Ragnarok', 0, 1)        
        cast_time = ragnarok.cast_time
        fading = ragnarok.cast_args[0]
        for i in range(cast_time - 1):
            self.g.main_loop_once() 

        footman0 = self.b.place_unit(self.footman_card, self.p0, (0,0))
        footman1 = self.b.place_unit(self.footman_card, self.p0, (0,1))
        footman2 = self.b.place_unit(self.footman_card, self.p0, (1,1))
        footman3 = self.b.place_unit(self.footman_card, self.p0, (3,2))
        footman4 = self.b.place_unit(self.footman_card, self.p1, (2,2))
        self.g.main_loop_once()

        # kill off footmen on row 2
        self.assertTrue(self.b.get_unit_position(footman0), None)
        self.assertTrue(self.b.get_unit_position(footman1), None)        
        self.assertTrue(self.b.get_unit_position(footman2), None)
        self.assertEquals(self.b.get_unit_position(footman3), None)
        self.assertEquals(self.b.get_unit_position(footman4), None)

        # run for fading duration turns, check that there are 5 footmen,
        # and 2 of them are out of will
        for i in range(fading):
            self.g.main_loop_once()
  
        footmen_will = [unit._ammo for unit in self.b.grid.values()]
        footmen_will.sort()
        self.assertEquals(len(footmen_will), fading)
        self.assertEquals(footmen_will[0:2], [0, 0])

    def test_trebuchet_build(self):
        """
        Tests that a trebuchet will kill a 15 hp footman in 2 turns
        and a 100 hp building in 4 turns
        """
        self.b.field_length = 11
        self.p1.gold = 9999
        self.p1.hand.append(Card.get_card('Econ'))
        self.g.play_building('Econ', 1, 0)
        trebuchet = self.b.place_unit(self.trebuchet_card, self.p0, (0,0))
        footman = self.b.place_unit(self.footman_card, self.p1, (6,0))
        trebuchet_damage = self.trebuchet_card.damage
        trebuchet_bdamage = self.trebuchet_card.combat_effect_args[0] + \
            trebuchet_damage
        trebuchet_range = self.trebuchet_card.attack_pattern[0][0]

        self.g.main_loop_once()
        self.assertEquals(self.b.grid[5,0]._hp, 
            self.footman_card.hp - trebuchet_damage) 

        self.assertEquals(self.p1._health, 55)
        self.assertEquals(self.b.buildings[1][0]._hp, 100)

        for i in range(self.b.field_length - trebuchet_range + 1):
            self.g.main_loop_once() # inch the trebuchet forward

        self.assertEquals(self.p1._health, 55)
        self.assertEquals(self.b.buildings[1][0]._hp, 75) # does 25 damage!


if __name__ == "__main__":
    unittest.main()

