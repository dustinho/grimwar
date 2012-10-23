import json
import os

class Grimoire:
    # keeps track of a player's Grimoire, 
    # instantiate it with a dict of "cardname":number
    def __init__(self, my_grimoire="all_cards"):
        spec_file = os.path.join(os.path.dirname(__file__), 'Grimoires', 
                                 my_grimoire + ".json")
        self.library = {}
        self.library = json.load(open(spec_file))
        
    def remove_from_grimoire(self, card_name):
        if self.library[card_name] < 1:
            assert False, "not enough cards left in grimoire"
        self.library[card_name] += -1

    def add_to_grimoire(self, card_name):
        self.library[card_name] += 1

