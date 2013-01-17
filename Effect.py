from Player import *
from Board import *
from Unit import *
from Preds import preds
from Modifier import *
from EffectUtils import *

class Effect:
    """
    Effects let you define a effect to apply in json. Game should test the
    trigger conditions for a card's effect, and if they apply, call applyEffect
    with the relevant args.
    """
    @staticmethod
    def applyEffect(effect_name, player, opponent, instance, board, args):
        return getattr(Effect, effect_name)(
            player,
            opponent,
            instance,
            board,
            args
        )

    @staticmethod
    def draw(player, opponent, instance, board, args):
        """
        @param Cards to draw
        """
        cards_to_draw = args[0]
        for x in xrange(cards_to_draw):
            player.draw()

    @staticmethod
    def heal_row(player, opponent, instance, board, args):
        """
        @param Heal amount
        """
        row = board.get_row_for_spell(player,instance)
        amount = args[0]
        units = board.get_units_with_preds(preds["row"](row),
            preds["owner"](player))
        for unit in units:
            unit.heal(amount)

    @staticmethod
    def upgrade_economy(player, opponent, instance, board, args):
        """
        Upgrades T1 workers to T2.
        If upgrade is T2, also upgrades T2 workers to T3.

        @param Upgrade level
        """
        upgrade_level = args[0]
        if upgrade_level >= 2:
            workers_to_upgrade = len(
                [card for card in player.discard_pile if card.name == \
                "SPeasant"]
            )
            player.discard_pile = deque([
                card for card in player.discard_pile \
                if not card.name == "SPeasant"])
            for x in xrange(workers_to_upgrade):
                player.discard_pile.append(Card.get_card("UPeasant"))

        if upgrade_level >= 1:
            workers_to_upgrade = len(
                [card for card in player.discard_pile if card.name == \
                "Peasant"]
            )
            player.discard_pile = deque([
                card for card in player.discard_pile \
                if not card.name == "Peasant"])
            for x in xrange(workers_to_upgrade):
                player.discard_pile.append(Card.get_card("SPeasant"))

    @staticmethod
    def buff_row_stats(player, opponent, instance, board, args):
        """
        Increases a row's attack/ammo/hp/movement for some number of turns.
        @param attack buff amount
        @param ammo buff amount
        @param hp (current and max) buff amount
        @param movement buff amount
        @param number of turns this buff lasts
        """
        plus_attack = args[0]
        plus_ammo = args[1]
        plus_hp = args[2]
        plus_movement = args[3]
        duration = args[4]
        row = board.get_row_for_spell(player, instance)
        units = board.get_units_with_preds(preds["row"](row),
            preds["owner"](player))
        for unit in units:
            buff_stats_modifier = BuffStatsModifier(
                plus_attack,
                plus_ammo,
                plus_hp,
                plus_movement,
                duration)
            buff_stats_modifier.attach(unit)

    @staticmethod
    def debuff_row_stats(player, opponent, instance, board, args):
        """
        Increases a row's attack/ammo/hp/movement for some number of turns.
        @param attack debuff amount
        @param ammo debuff amount
        @param hp (current and max) debuff amount
        @param movement debuff amount
        @param number of turns this debuff lasts
        """
        plus_attack = args[0]
        plus_ammo = args[1]
        plus_hp = args[2]
        plus_movement = args[3]
        duration = args[4]
        row = board.get_row_for_spell(player, instance)
        units = board.get_units_with_preds(preds["row"](row),
            preds["owner"](player))
        for unit in units:
            debuff_stats_modifier = DebuffStatsModifier(
                plus_attack,
                plus_ammo,
                plus_hp,
                plus_movement,
                duration)
            debuff_stats_modifier.attach(unit)


    @staticmethod
    def tech_level(player, opponent, instance, board, args):
        """
        Attaches a modifier to the current player that grants it the ability
        to buy cards equal to or below a given tech level for a turn.

        @param Faction
        @param Tech level (2 or 3)
        """
        tech_faction = args[0]
        tech_level = args[1]
        tech_modifier = TechLevelModifier(tech_faction, tech_level)
        tech_modifier.attach(player)

    @staticmethod
    def ragnarok(player, opponent, instance, board, args):
        """
        Destroys all units in the row to the right.  Copies over
        all allied units to that row, and gives them all fading
        for some turns

        @param fading length
        """
        spell_row = board.get_row_for_spell(player, instance)
        target_row = board.get_row_to_right(spell_row, player)
        target_units = board.get_units_with_preds(preds["row"](spell_row),
            preds["owner"](player)) # this will copy heroes, as well!
        if not target_row:
            return

        EffectUtils.destroy_row(target_row, board)
        for unit in target_units:
            position = board.get_unit_position(unit)
            new_position = board.get_hex_to_right(position, player)
            if not board.is_empty_for_units(new_position):
                continue
            new_unit = unit.clone()
            board.grid[new_position] = new_unit
            fading_modifier = FadingModifier(args[0])
            fading_modifier.attach(new_unit)

    @staticmethod
    def give_protection(player, opponent, instance, board, args):
        """
        Whenever unit in front takes damage, this unit takes some amount of
        damage instead.

        @param protect amount
        """
        amount = args[0]
        position = board.get_unit_position(instance)
        space_ahead = (position[0]+1, position[1])

        target = board.grid.get(space_ahead)
        if target:
            protection = ProtectionModifier(instance, amount)
            protection.attach(target)




