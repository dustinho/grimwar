from Player import *
from Board import *
from Unit import *
from Preds import preds
from Modifier import *

class CombatEffect:
    """
    CombatEffects are just effects that trigger during the combat phase, so
    they have a different set of natural arguments. It is checked after one
    unit hits another.
    """
    @staticmethod
    def applyCombatEffect(effect_name, attacker, defender, board, args):
        return getattr(CombatEffect, effect_name)(
            attacker,
            defender,
            board,
            args
        )


class DefensiveEffect:
    """
    Effects that are checked when the unit takes a hit.
    """
    @staticmethod
    def applyDefensiveEffect(effect_name, attacker, defender, board, args):
        return getattr(DefensiveEffect, effect_name)(
            attacker,
            defender,
            board,
            args
        )

    @staticmethod
    def stalwart(attacker, defender, board, args):
        """
        Hitting this unit removes an additional will
        """
        attacker._ammo -= 1
        return




