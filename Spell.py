from Card import *
from Player import *

class Spell:
    """
    Spells are the manifestation of a played SpellCard on the board.
    """

    @staticmethod
    def get_spell(card, owner):
        return Spell(card, owner)

    def __init__(self, card, owner):
        assert isinstance(card, SpellCard), \
            "card is not a SpellCard: {0}".format(card)
        assert isinstance(owner, Player), \
            "owner is not a Player: {0}".format(Player)
        self.card = card
        self.cast_time = self.card.cast_time
        self.cast_effect = self.card.cast_effect
        self.cast_args = self.card.cast_args

        self.cast_time_remaining = self.cast_time

        self.owner = owner

    def __str__(self):
        return "<{0}, {1} cast_time_remaining>".format(
            self.card.name,
            self.cast_time_remaining
        )
