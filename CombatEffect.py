from Player import *
from Board import *
from Unit import *
from Building import *
from Preds import preds
from Modifier import *


def affects_buildings(effect):
    effect.affects_buildings = True
    return effect


def affects_players(effect):
    effect.affects_players = True
    return effect


class CombatEffect:
    """
    CombatEffects are just effects that trigger during the combat phase, so
    they have a different set of natural arguments. It is checked after one
    unit hits something.  If the other target is a player or building,
    the effect only activates if the effect function has @affects_players or
    @affects_buildings, respectively. Otherwise, the target is a unit,
    and the effect happens.
    """
    @staticmethod
    def applyCombatEffect(effect_name, attacker, defender, board, args):
        effect = getattr(CombatEffect, effect_name)
        if isinstance(defender, Player):
            if hasattr(effect, "affects_players"):
                return effect(
                    attacker,
                    defender,
                    board,
                    args
                    )
        elif isinstance(defender, Building):
            if hasattr(effect, "affects_buildings"):
                return effect(
                    attacker,
                    defender,
                    board,
                    args
                    )
        else:  # Defender is probably a Unit
            return effect(
                    attacker,
                    defender,
                    board,
                    args
                    )
        return

    @staticmethod
    @affects_buildings
    def siege(attacker, defender, board, args):
        """
        If defender is a building, do bonus damage to It

        @param Amount of bonus damage
        """
        if isinstance(defender, Building):
            defender.take_damage(args[0])
        return


class DefensiveEffect:
    """
    Effects that are checked when the unit takes a hit.
    """
    @staticmethod
    def applyDefensiveEffect(effect_name, attacker, defender, board, args):
        effect = getattr(DefensiveEffect, effect_name)
        if isinstance(attacker, Player):
            if hasattr(effect, "affects_players"):
                return effect(
                    attacker,
                    defender,
                    board,
                    args
                    )
        elif isinstance(attacker, Building):
            if hasattr(effect, "affects_buildings"):
                return effect(
                    attacker,
                    defender,
                    board,
                    args
                    )
        else:
            return effect(
                    attacker,
                    defender,
                    board,
                    args
                    )
        return

    @staticmethod
    def stalwart(attacker, defender, board, args):
        """
        Hitting this unit removes an additional will
        """
        attacker._ammo -= 1
        return



