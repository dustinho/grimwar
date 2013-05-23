from Card import *
from Player import *

class Building:
    """
    Building are the manifestation of a played BuildingCard on the board.
    """

    @staticmethod
    def get_building(card, owner):
        return Building(card, owner)

    def __init__(self, card, owner):
        assert isinstance(card, BuildingCard), \
            "card is not a BuildingCard: {0}".format(card)
        assert isinstance(owner, Player), \
            "owner is not a Player: {0}".format(Player)
        self.card = card
        self._hp = card.hp
        self.combat_effect = self.card.combat_effect
        self.combat_effect_args = self.card.combat_effect_args
        self.defensive_effect = self.card.defensive_effect
        self.defensive_effect_args = self.card.defensive_effect_args
        self.upkeep_effect = card.upkeep_effect
        self.upkeep_effect_args = card.upkeep_effect_args

        self.owner_id = owner.id
        self.modifiers = []

    def __str__(self):
        return "<{0}>".format(
            self.card.name
        )

    def take_damage(self, damage_amount):
        self._hp = self._hp - damage_amount

    def get_curr_hp(self):
        return self._hp

