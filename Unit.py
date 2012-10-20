class Unit:
    """
    A Unit is a representation of what a played card summons to the Board.
    It has a base card it was created from, tracks the result of actions
    performed on it (damage, loss of ammo, modifiers applied).

    TODO later:
    Modifiers
    """

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



