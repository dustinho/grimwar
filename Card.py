import json
import os

class Card:
    """
    The Card class represents an instance of a card (in a players hand, deck,
    ect). Card interactions are handled by a CardManager and are converted to
    a Unit when placed on a Board. Card data is specificed in an associated
    JSON file.

    Cards are immutable.
    """

    def __init__(self, name):
        spec_file = self.get_card_path(name)
        self.name = self.ammo = self.cost = self.hp = self.speed = self.damage = self.attack_pattern = self.attack_type = self.tier = self.buy_cost = None

        data = json.load(open(spec_file))

        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])

    def __str__(self):
        """return a string describing the Card"""
        return "<{0} Card>".format(self.name)

    def get_card_path(self, name):
        return os.path.join(os.path.dirname(__file__), 'Cards', name + ".json")

class WorkerCard(Card):
    """
    WorkerCard is a special card. Its JSON is loaded from the /Cards/Workers
    directory
    """
    def get_card_path(self, name):
        return os.path.join(os.path.dirname(__file__), 'Cards', 'Workers', name + ".json")
    def __init__(self, name):
        Card.__init__(self, name)

class HeroCard(Card):
    """
    HeroCard is a special card.  Its JSON is loaded from the /Cards/Heroes
    directory
    """
    def get_card_path(self, name):
        return os.path.join(os.path.dirname(__file__), 'Cards', 'Heroes', name + ".json")
    def __init__(self, name):
        Card.__init__(self, name)
