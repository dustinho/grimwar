from Card import Card
from Player import Player

class Unit:
    """
    A Unit is a representation of what a played card summons to the Board.
    It has a base card it was created from, tracks the result of actions
    performed on it (damage, loss of ammo, modifiers applied).

    TODO later:
    Modifiers
    """

    def __init__(self, card, owner):
        assert isinstance(card, Card), "card is not a Card: {0}".format(card)
        assert isinstance(owner, Player), "owner is not a Player: {0}".format(Player)
        self.card = card
        self._hp = self.card.hp
        self._ammo = self.card.ammo
        self._speed = self.card.speed
        self._damage = self.card.damage
        self._attack_pattern = self.card.attack_pattern
        self._attack_type = self.card.attack_type
        self.owner = owner

    def __str__(self):
        return "<{0}, {1} hp, {2} ammo>".format(self.card.name, self.get_curr_hp(), self.get_curr_ammo())

    def get_curr_hp(self):
        return self._hp

    def get_max_hp(self):
        return self.card.hp

    def get_curr_ammo(self):
        return self._ammo

    def get_max_ammo(self):
        return self.card.ammo

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
        return self._attack_pattern

    def get_attack_type(self):
        # "single" attacks first enemy unit in range, "splash" attacks all in range
        return self._attack_type

class Worker(Unit):
    def __init__(self, card, owner):
        Unit.__init__(self, card, owner)
        self._waypoints = 0

    def get_waypoints(self):
        # keeps track of how many waypoints the worker has reached
        return self._waypoints

class Hero(Unit):
    def __init(self, card, owner):
        Unit.__init__(self, card, owner)
        assert isinstance(card, HeroCard)
