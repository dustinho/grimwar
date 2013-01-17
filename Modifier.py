import traceback

class Modifier:
    """
    Modifiers affect a unit or player and are stored inside the objects it
    modifies. Modifiers define a modification to be made to the object, the
    the way to reverse the modification, as well as the conditions in which
    the modification should be reversed. Modifiers will also each get called
    during upkeep to perform whatever logic they may need.

    Modifiers synergize with Effects. Many effects will place a modifier on
    specific units, knowing that the modifier will fade at the end of the turn.

    Use modifiers to perform complicated effects - if there's something simple
    and permanent you wish to do, you can probably implement it much easier as
    a pure Effect.
    """
    def attach(self, target):
        target.modifiers.append(self)
        self.target = target

    def upkeepLogic(self, board):
        """
        This gets called every upkeep
        """
        self.remove()

    def cleanupLogic(self, board):
        """
        This determines whether a spell should be removed or not. This should
        not modify state, as it will be repeatedly called.
        """
        return

    def remove(self):
        self.target.modifiers.remove(self)

class BuffStatsModifier(Modifier):
    """This modifier buffs attk/ammo/hp(curr and max)/movement
    of a unit for a certain number of turns"""
    def __init__(self, plus_attack, plus_ammo, plus_hp, plus_movement, turns):
        self.plus_attack = plus_attack
        self.plus_ammo = plus_ammo
        self.plus_hp = plus_hp
        self.plus_movement = plus_movement
        self.turns_left = turns

    def attach(self, target):
        target._damage += self.plus_attack
        target._ammo += self.plus_ammo
        target._hp += self.plus_hp
        target._max_hp += self.plus_hp
        target._speed += self.plus_movement
        target._remaining_moves += self.plus_movement
        Modifier.attach(self, target)

    def upkeepLogic(self, board):
        self.turns_left -= 1
        self.cleanupLogic(board)

    def cleanupLogic(self, board):
        if self.turns_left <= 0:
            self.remove()

    def remove(self):
        self.target._damage -= self.plus_attack
        self.target._ammo -= self.plus_ammo
        self.target._hp -= self.plus_hp
        self.target._max_hp -= self.plus_hp
        self.target._speed -= self.plus_movement
        self.target._remaining_moves -= self.plus_movement
        Modifier.remove(self)

class DebuffStatsModifier(Modifier):
    """This modifier debuffs attk/ammo/hp(curr and max)/movement
    of a unit for a certain number of turns"""
    def __init__(self, minus_damage, minus_ammo, minus_hp, minus_movement, turns):
        self.minus_damage = minus_damage
        self.minus_ammo = minus_ammo
        self.minus_hp = minus_hp
        self.minus_movement = minus_movement
        self.turns_left = turns

    def attach(self, target):
        target._damage -= self.minus_damage
        target._ammo -= self.minus_ammo
        target._hp -= self.minus_hp
        target._max_hp -= self.minus_hp
        target._speed -= self.minus_movement
        target._remaining_moves -= self.minus_movement
        Modifier.attach(self, target)

    def upkeepLogic(self, board):
        self.turns_left -= 1
        self.cleanupLogic(board)

    def cleanupLogic(self, board):
        if self.turns_left <= 0:
            self.remove()

    def remove(self):
        self.target._damage += self.minus_damage
        self.target._ammo += self.minus_ammo
        self.target._hp += self.minus_hp
        self.target._max_hp += self.minus_hp
        self.target._speed += self.minus_movement
        self.target._speed += self.minus_movement
        Modifier.remove(self)


class TechLevelModifier(Modifier):
    """
    Grimoires will check if an TechLevelModifier of the right level exists
    before allowing a player to buy a card.
    """
    def __init__(self, faction, level):
        self.faction = faction
        self.level = level

    def attach(self, target):
        Modifier.attach(self, target)


class AmbushModifier(Modifier):
    """
    When a unit is ambushed, this modifier is applied to it.
    Reduces movement speed to 0 for the rest of the turn.
    """
    def attach(self, target):
        target.use_all_moves()

class FadingModifier(Modifier):
    """
    Keeps an internal counter of how long unit has been fading.
    When the fading duration ends, the unit gets will = 0.
    """
    def __init__(self, turns):
        self.turns_left = turns

    def attach(self, target):
        Modifier.attach(self, target)

    def upkeepLogic(self, board):
        self.turns_left -= 1
        self.cleanupLogic(board)

    def cleanupLogic(self, board):
        if self.turns_left <= 0:
            self.remove(board)

    def remove(self, board):
        self.target.ammo = 0
        Modifier.remove(self)

class ProtectionModifier(Modifier):
    """
    When a unit protects another unit, whenever the target unit takes damage
    the protector takes a certain amount of damage instead of the unit.

    Let's not bounce units. So many modifiers could get fucked up if we have a
    bounce.
    """
    def __init__(self, protector, amount):
        self.protector = protector
        self.amount = amount

    def attach(self, target):
        Modifier.attach(self, target)


