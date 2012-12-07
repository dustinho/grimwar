import sys
sys.path.append('../')
sys.path.append('../TK_UIv2/')

from UserInputTypes import PutCard, Reset, Next

import pickle

class SimulatorActions:
    def __init__(self, protocol):
        self.protocol = protocol

    def put_card_in_play(self, player_id, card, location):
        pc = PutCard(player_id, card, location)
        ppc = pickle.dumps(pc)
        self.protocol.sendString(ppc)

    def reset(self):
        r = Reset()
        pr = pickle.dumps(r)
        self.protocol.sendString(pr)
    
    def next(self):
        n = Next()
        pn = pickle.dumps(n)
        self.protocol.sendString(pn)
