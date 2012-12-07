from UserInputTypes import PlayCard, BuyCard

import pickle

class PlayerActions:
    def __init__(self, protocol):
        self.protocol = protocol

    def play_card(self, player_id, card, location):
        pc = PlayCard(player_id, card, location)
        ppc = pickle.dumps(pc)
        self.protocol.sendString(ppc)
        
    def buy_card(self, player_id, card_name):
        bc = BuyCard(player_id, card_name)
        pbc = pickle.dumps(bc)
        self.protocol.sendString(pbc)
    
