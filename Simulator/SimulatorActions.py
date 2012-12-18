import sys
sys.path.append('../')
sys.path.append('../TK_UIv2/')

from Actions import Actions
from UserInputTypes import Reset, Next

import pickle

class SimulatorActions(Actions):
    def __init__(self, protocol):
        self.protocol = protocol

    def reset(self):
        r = Reset()
        pr = pickle.dumps(r)
        self.protocol.sendString(pr)
    
    def next(self):
        n = Next()
        pn = pickle.dumps(n)
        self.protocol.sendString(pn)
