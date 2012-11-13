import json
import os
from Card import Card

class Grimoire:
    # keeps track of a player's Grimoire,
    # instantiate it with a dict of "cardname":number
    def __init__(self, my_grimoire="all_cards"):
        spec_file = os.path.join(os.path.dirname(__file__), 'Grimoires',
                                 my_grimoire + ".json")
        self.library = {}
        self.library = json.load(open(spec_file))
        self.cards = {}
        self._create_card_examples()

    def get_buyable_card_names(self):
        return [x for x in self.library.iterkeys() if self.library[x] >= 1]

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
    
