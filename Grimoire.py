import json
import os
from Modifier import *
from Card import Card


class Grimoire:
    # keeps track of a player's Grimoire,
    # instantiate it with a dict of "cardname":number
    def __init__(self, owner, my_grimoire="all_cards"):
        spec_file = os.path.join(os.path.dirname(__file__), 'Grimoires',
                                 my_grimoire + ".json")
        self.library = {}
        self.library = json.load(open(spec_file))
        self.cards = {}
        self._create_card_examples()

    def get_buyable_card_names(self, owner):
        # Compute max tier level for each faction
        tech_levels = {}
        for modifier in owner.modifiers:
            if isinstance(modifier, TechLevelModifier) and \
                modifier.level > tech_levels.get(modifier.faction, 0):
                tech_levels[modifier.faction] = modifier.level

        return [x for x in self.library.iterkeys() if self.is_buyable(x, tech_levels)]

    def is_buyable(self, card_name, tech_levels):
        if (self.library[card_name] < 1):
            return False
        faction = self.cards[card_name].faction
        tier = self.cards[card_name].tier
        if faction != 'neutral':
            return tech_levels.get(faction, 1) >= tier
        elif faction == 'neutral':
            if len(tech_levels) == 0:
                return 1 >= tier
            else:
                return max(tech_levels.values(), 1) >= tier
        return True

    def remove_from_grimoire(self, card_name):
        if self.library[card_name] < 1:
            raise ValueError("not enough cards left in grimoire")
        self.library[card_name] += -1

    def add_to_grimoire(self, card_name):
        self.library[card_name] += 1

    def _create_card_examples(self):
        # access example cards with grimoire["cardname"]
        for i in self.library.keys():
            self.cards[i] = Card.get_card(i)

