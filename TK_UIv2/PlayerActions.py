from Actions import Actions
from UserInputTypes import BuyCard

import pickle

class PlayerActions(Actions):
        
    def buy_card(self, player_id, card_name):
        bc = BuyCard(player_id, card_name)
        pbc = pickle.dumps(bc)
        self.protocol.sendString(pbc)
    
