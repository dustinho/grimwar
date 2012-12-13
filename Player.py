from collections import deque
from Grimoire import Grimoire
from Card import Card
import random
import logging

class Player:
    STARTING_HEALTH = 55
    INVALID_PLAYER = 0
    FACING_LEFT = 1
    FACING_RIGHT = 2
    STARTING_GOLD = 20

    def __init__(self, id):
        self.id = id
        self.reset()

    def __str__(self):
        lines = []
        lines.append("Health: {0}".format(self.get_curr_health()))
        lines.append("Gold: {0}".format(self.gold))
        lines.append("Hand: {0}".format(", ".join([str(x) for x in self.hand])))
        lines.append("Deck: {0}".format(", ".join([str(x) for x in self.deck])))
        lines.append("Discard Pile: {0}".format(", ".join(
            [str(x) for x in self.discard_pile]
        )))
        return "\n".join(lines)

    def buy(self, card_name):
        if (self.spend_gold(Card.get_card(card_name).buy_cost)):
            self.grimoire.remove_from_grimoire(card_name)
            self.discard_pile.append(Card.get_card(card_name))

    def play(self, card_name):
        # find the card in hand
        card = self.find_card(card_name, self.hand)
        self.spend_gold(card.cost)
        self.inplay.append(card)
        self.hand.remove(card)
        return card

    def draw(self):
        if len(self.deck) == 0:
            if len(self.discard_pile) == 0:
                return
            self.deck = self.discard_pile
            self.discard_pile = deque()
            random.shuffle(self.deck)
        self.hand.append(self.deck.popleft())

    def discard(self, card):
        self.hand.remove(card)
        self.discard_pile.append(card)

    def unit_died(self, unit):
        self.inplay.remove(unit.card)
        self.discard_pile.append(unit.card)

    def hero_died(self, hero):
        self.inplay.remove(hero.card)
        self.deck.appendleft(hero.card)

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
        self.discard_pile = deque(discard_pile)

    def set_deck(self, deck):
        self.deck = deque(deck)

    def set_hand(self, hand):
        self.hand = deque(hand)

    def set_inplay(self, inplay):
        self.inplay = deque(inplay)

    def set_library(self, library):
        self.grimoire.library = library

    def set_gold(self, amount):
        self.gold = amount

    def reset(self):
        self.deck = deque()
        self.discard_pile = deque()
        self.hand = deque()
        self.inplay = deque()
        self._health = Player.STARTING_HEALTH
        self.set_direction(Player.FACING_RIGHT)
        self.gold = Player.STARTING_GOLD
        self.grimoire = Grimoire()

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



