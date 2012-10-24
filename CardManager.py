from collections import deque
import random

class CardManager:
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

    def setDiscardPile(self, discard_pile):
        self.discard_pile = deque(discard_pile)

    def setDeck(self, deck):
        self.deck = deque(deck)

    def setHand(self, hand):
        self.hand = deque(hand)

    def reset(self):
        self.deck = deque()
        self.discard_pile = deque()
        self.hand = deque()



