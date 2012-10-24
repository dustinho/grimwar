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
        spec_file = os.path.join(__file__, 'Cards', name + ".json")
        self.name = self.ammo = self.cost = self.hp = None

        data = json.load(open(spec_file))

        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])

