import Card
import Player

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

    def get_speed(self)
        return self._speed


