from Grimoire import Grimoire
from Card import Card
from Unit import *
import random
import logging

class Player:
    STARTING_HEALTH = 100
    INVALID_PLAYER = -1
    FACING_LEFT = 1
    FACING_RIGHT = 0
    STARTING_GOLD = 20
    MAX_HAND_SIZE = 5

    def __init__(self, id):
        self.id = id
        self.reset()

    def reset(self):
        self.deck = []
        self.discard_pile = []
        self.hand = []
        self.inplay = []
        self._health = Player.STARTING_HEALTH
        self.set_direction(Player.FACING_RIGHT)
        self.gold = Player.STARTING_GOLD
        self.grimoire = Grimoire(self, 'play')
        self.modifiers = []

    def __str__(self):
        lines = []
        lines.append("Health: {0}".format(self.get_curr_health()))
        lines.append("Gold: {0}".format(self.gold))
        lines.append("Hand: {0}".format(", ".join([str(x) for x in self.hand])))
        return "\n".join(lines)

    def buy(self, card_name):
        if (self.spend_gold(Card.get_card(card_name).buy_cost)):
            self.grimoire.remove_from_grimoire(card_name)
            self.discard_pile.append(Card.get_card(card_name))

    def play(self, card_name, spend_gold=True):
        # find the card in hand
        card = self.find_card(card_name, self.hand)
        if spend_gold:
            if not self.spend_gold(card.cost):
                logging.debug("Attempted to play {0} without sufficient funds".format(card_name))
                return None
        self.inplay.append(card)
        self.hand.remove(card)
        return card

    def draw(self):
        if len(self.deck) == 0:
            if len(self.discard_pile) == 0:
                return
            self.deck = self.discard_pile
            self.discard_pile = []
            random.shuffle(self.deck)
        if len(self.hand) < self.MAX_HAND_SIZE:
            self.hand.append(self.deck.pop(0))

    def discard(self, card):
        self.hand.remove(card)
        self.discard_pile.append(card)

    def unit_died(self, unit):
        if unit.card in self.inplay:
            if isinstance(unit, Hero):
                self.inplay.remove(unit.card)
                self.deck.insert(0, unit.card)
            else:
                self.inplay.remove(unit.card)
                self.discard_pile.append(unit.card)

    def spell_remove(self, spell):
        self.inplay.remove(spell.card)
        self.discard_pile.append(spell.card)

    def spend_gold(self, amount):
        """
        Attempts to spend gold. Returns false if there is not enough gold to
        spend.
        """
        if amount > self.gold:
            return False
        self.gold -= amount
        return True

    def find_card(self, card_name, collec):
        # returns the first card object that matches card name from collec
        if card_name not in [c.name for c in collec]:
            assert False, "{0} not in {1}".format(card_name, collec)
        return [c for c in collec if c.name == card_name][0]

    ## Setters

    def set_discard_pile(self, discard_pile):
        self.discard_pile = discard_pile

    def set_deck(self, deck):
        self.deck = deck

    def set_hand(self, hand):
        self.hand = hand

    def set_inplay(self, inplay):
        self.inplay = inplay

    def set_gold(self, amount):
        self.gold = amount

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def get_curr_health(self):
        return self._health

    def take_damage(self, damage_amount):
        self._health = self._health - damage_amount
        logging.info("Player {0} at {1} health".format(
            self.id,
            self.get_curr_health()
        ))



