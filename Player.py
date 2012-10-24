from collections import deque
import random

STARTING_HEALTH = 20
FACING_LEFT = 0
FACING_RIGHT = 1

class Player:
    def __init__(self):
        self.reset()

    def __str__(self):
        lines = []
        lines.append("Hand: {0}".format(self.hand))
        lines.append("Deck: {0}".format(self.deck))
        lines.append("Discard Pile: {0}".format(self.discard_pile))
        return "\n".join(lines)

    def buy(self, card):
        self.discard_pile.append(card)

    def draw(self):
        if len(self.deck) == 0:
            self.deck = self.discard_pile[:]
            self.discard_pile = deque()
            random.shuffle(self.deck)
        self.hand.append(self.deck.popleft())

    def discard(self, card):
        self.hand.remove(card)
        self.discard_pile.append(card)

    ## Setters

    def set_discard_pile(self, discard_pile):
        self.discard_pile = deque(discard_pile)

    def set_deck(self, deck):
        self.deck = deque(deck)

    def set_hand(self, hand):
        self.hand = deque(hand)

    def set_inplay(self, inplay):
        self.inplay = deque(inplay)

    def reset(self):
        self.deck = deque()
        self.discard_pile = deque()
        self.hand = deque()
        self.inplay = deque()
        self.health = STARTING_HEALTH
        self.set_direction(FACING_RIGHT)

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction


