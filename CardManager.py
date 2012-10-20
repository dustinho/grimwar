from collections import deque
import random

class CardManager:
    def __init__(self):
        self.reset()

    def __str__(self):
        ret = ""
        ret += "Hand: " + str(self.hand) + "\n"
        ret += "Deck: " + str(self.deck) + "\n"
        ret += "Discard: " + str(self.discard)
        return ret

    def buy(self, card):
        self.discard.append(card)

    def draw(self):
        if len(self.deck) == 0:
            self.deck = self.discard[:]
            self.discard = deque()
            random.shuffle(self.deck)
        self.hand.append(self.deck.popleft())

    def discardCard(self, card):
        self.hand.remove(card)
        self.discard.append(card)

    def setDiscard(self, discard):
        self.discard = deque(discard)

    def setDeck(self, deck):
        self.deck = deque(deck)

    def setHand(self, hand):
        self.hand = deque(hand)

    def reset(self):
        self.deck = deque()
        self.discard = deque()
        self.hand = deque()



