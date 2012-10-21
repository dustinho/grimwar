
class Grimoire:
    # keeps track of a player's Grimoire, 
    # instantiate it with a dict of "cardname":number
    def __init__(self, my_grimoire):
        self.grimoire = my_grimoire
        
    def remove_from_grimoire(self, card_name):
        if self.grimoire[card_name] < 1:
            assert False, "not enough cards left in grimoire"
        self.grimoire[card_name] += -1

    def add_to_grimoire(self, card_name):
        self.grimoire[card_name] += 1

