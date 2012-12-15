from UserInputTypes import PlayUnitCard, PlaySpellCard, PlayBuildingCard, BuyCard

import pickle

class PlayerActions:
    def __init__(self, protocol):
        self.protocol = protocol

    def play_unit_card(self, player_id, card, location):
        puc = PlayUnitCard(player_id, card, location)
        ppuc = pickle.dumps(puc)
        self.protocol.sendString(ppuc)

    def play_spell_card(self, player_id, card, slot):
        psc = PlaySpellCard(player_id, card, slot)
        ppsc = pickle.dumps(psc)
        self.protocol.sendString(ppsc)

    def play_building_card(self, player_id, card, slot):
        pbc = PlayBuildingCard(player_id, card, slot)
        ppbc = pickle.dumps(pbc)
        self.protocol.sendString(ppbc)
        
    def buy_card(self, player_id, card_name):
        bc = BuyCard(player_id, card_name)
        pbc = pickle.dumps(bc)
        self.protocol.sendString(pbc)
    
