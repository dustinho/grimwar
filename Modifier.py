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
        return

    def cleanupLogic(self, board):
        """
        This function gets run in the cleanup phase. Usually you should
        determine if the modifier needs to be removed here. By default all
        modifiers expire upon end of turn.
        """
        self.remove()

    def remove(self):
        self.target.modifiers.remove(self)

class AttackModifier(Modifier):
    """
    This modifier pumps a unit's attack for a certain number of turns.
    """
    def __init__(self, plus_attack, turns):
        self.plus_attack = plus_attack
        self.turns_left = turns

    def attach(self, target):
        target._damage += self.plus_attack
        Modifier.attach(self, target)

    def cleanupLogic(self, board):
        self.turns_left -= 1
        if self.turns_left <= 0:
            self.remove()

    def remove(self):
        self.target._damage -= self.plus_attack
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
