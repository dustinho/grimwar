from Card import *
from Modifier import *
import copy
import logging

class Unit:
    """
    A Unit is a representation of what a played card summons to the Board.
    It has a base card it was created from, tracks the result of actions
    performed on it (damage, loss of ammo, modifiers applied).

    TODO later:
    Modifiers
    """

    @staticmethod
    def get_unit(card, owner):
        if isinstance(card, HeroCard):
            return Hero(card, owner)
        elif isinstance(card, WorkerCard):
            return Worker(card, owner)
        else:
            return Unit(card, owner)

    def __init__(self, card, owner):
        assert isinstance(card, Card), "card is not a Card: {0}".format(card)
        self.card = card
        self._hp = self.card.hp
        self._max_hp = self.card.hp
        self._ammo = self.card.ammo
        self._speed = self.card.speed
        self._damage = self.card.damage
        self._attack_pattern = self.card.attack_pattern
        self._attack_type = self.card.attack_type
        self._remaining_moves = self._speed
        self._ready = True
        self.owner = owner

        self.combat_effect = self.card.combat_effect
        self.combat_effect_args = self.card.combat_effect_args
        self.defensive_effect = self.card.defensive_effect
        self.defensive_effect_args = self.card.defensive_effect_args
        self.upkeep_effect = self.card.upkeep_effect
        self.upkeep_effect_args = self.card.upkeep_effect_args

        self.modifiers = []

    def __str__(self):
        return "<{0}, {1} hp, {2} ammo>".format(self.card.name, self.get_curr_hp(), self.get_curr_ammo())

    def get_curr_hp(self):
        return self._hp

    def get_curr_hp(self):
        return self._hp

    def get_curr_ammo(self):
        return self._ammo

    def get_modifiers(self):
        # TODO
        return []

    def get_speed(self):
        # how many forward spaces the unit moves per turn (possibly fancier moves later)
        return self._speed

    def get_damage(self):
        # amount of damage dealt per attack
        return self._damage

    def get_attack_pattern(self):
        # an array of [x,y] coordinates it can attack if the unit is at [0,0]
        if self.owner.get_direction() == self.owner.FACING_RIGHT:
            return [ (x[0], x[1]) for x in self._attack_pattern ]
        else:
            return [ (-x[0], -x[1]) for x in self._attack_pattern ]

    def get_attack_type(self):
        # "single" attacks first enemy unit in range, "splash" attacks all in range
        return self._attack_type

    def is_ready(self):
        return self._ready

    def ready(self):
        self._ready = True

    def exhaust(self):
        self._ready = False

    def get_used_moves(self):
        return self._speed - self._remaining_moves

    def get_remaining_moves(self):
        return self._remaining_moves

    def use_move(self):
        self._remaining_moves -= 1

    def use_all_moves(self):
        self._remaining_moves = 0

    def refresh_moves(self):
        self._remaining_moves = self._speed

    def take_damage(self, damage_amount):
        for modifier in self.modifiers:
            if isinstance(modifier, ProtectionModifier):
                if damage_amount >= modifier.amount:
                    damage_amount -= modifier.amount
                    modifier.protector.take_damage(modifier.amount)
                else:
                    damage_amount = 0
                    modifier.protector.take_damage(damage_amount)
                logging.info("{0} was protected.".format(self.card.name))

        self._hp = self._hp - damage_amount
        if self._hp > self._max_hp:
            self._hp = self.card.hp

    def heal(self, amount):
        self._hp = self._hp + amount
        if self._hp > self._max_hp:
            self._hp = self.card.hp

    def spend_ammo(self, ammo_spent=1):
        self._ammo = self._ammo - ammo_spent

    def clone(self):
        """
        Returns a clone of self
        """
        new_unit = Unit.get_unit(self.card, self.owner)
        new_unit.card = self.card
        new_unit._hp = self._hp
        new_unit._max_hp = self._max_hp
        new_unit._ammo = self._ammo
        new_unit._speed = self._speed
        new_unit._damage = self._damage
        new_unit._attack_pattern = self._attack_pattern
        new_unit._attack_type = self._attack_type
        new_unit._remaining_moves = self._remaining_moves
        new_unit._ready = self._ready
        new_unit.owner = self.owner
        new_unit.modifiers = copy.deepcopy(self.modifiers)

        return new_unit

class Worker(Unit):
    def __init__(self, card, owner):
        Unit.__init__(self, card, owner)
        self.visited_sectors = []

class Hero(Unit):
    def __init(self, card, owner):
        Unit.__init__(self, card, owner)
        assert isinstance(card, HeroCard), "card is not a HeroCard: {0}".format(card)
