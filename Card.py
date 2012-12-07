import json
import os
import logging

class Card:
    """
    The Card class represents an instance of a card (in a players hand, deck,
    ect). Card interactions are handled by a CardManager and are converted to
    a Unit when placed on a Board. Card data is specificed in an associated
    JSON file.

    Cards are immutable.
    """
    @staticmethod
    def get_card(name):
        """Factory method that searches all card folders for the named card and
        returns an instance of the appropriate typed subclass of Card"""
        card_root = os.path.join(os.path.dirname(__file__), 'Cards')
        folders_and_types = [ (card_root, Card),
                              (os.path.join(card_root, "Workers"), WorkerCard),
                              (os.path.join(card_root, "Heroes"), HeroCard),
                            ]
        for (folder, klass) in folders_and_types:
            json_file_path = os.path.join(folder, name + ".json")
            logging.debug("trying {0}".format(json_file_path))
            if os.path.exists(json_file_path):
                return klass(json_file_path)
        raise ValueError("Couldn't find a file {0}.json".format(name))

    @staticmethod
    def get_all_cards_list():
        """Returns a list of Card objects, one for each type of card in the game"""
        #TODO: clean this up
        card_suffix = ".json"
        suf_len = len(card_suffix)
        card_root = os.path.join(os.path.dirname(__file__), 'Cards')
        raw_dir_list = os.listdir(card_root) 
        raw_dir_list.extend(os.listdir(os.path.join(card_root, "Workers")))
        raw_dir_list.extend(os.listdir(os.path.join(card_root, "Heroes")))
        return [Card.get_card(dir_entry[:-suf_len]) for dir_entry in raw_dir_list \
                if dir_entry.endswith(".json")]

    def __init__(self, spec_file):
        self.name = None
        self.ammo = None
        self.cost = None
        self.hp = None
        self.speed = None
        self.damage = None
        self.attack_pattern = None
        self.attack_type = None
        self.tier = None
        self.buy_cost = None
        self.faction = None
        self.archetype = None
        data = json.load(open(spec_file))

        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])

    def __str__(self):
        """return a string describing the Card"""
        return "<{0} Card>".format(self.name)


class WorkerCard(Card):
    """
    WorkerCard is a special card. Its JSON is loaded from the /Cards/Workers
    directory
    """
    def __init__(self, spec_file):
        Card.__init__(self, spec_file)

class HeroCard(Card):
    """
    HeroCard is a special card.  Its JSON is loaded from the /Cards/Heroes
    directory
    """
    def __init__(self, spec_file):
        Card.__init__(self, spec_file)
        self.level = 1
