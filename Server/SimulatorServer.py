from twisted.internet import reactor
from SimulatorController import SimulatorController
from ServerProtocol import ServerProtocolFactory
import sys
sys.path.append('../')
sys.path.append('../TK_UIv2')
from UserInputTypes import PlayBuildingCard, PlaySpellCard, PlayUnitCard
from UserInputTypes import Next, Reset

import pickle

class SimulatorServer:
    def __init__(self):
        self.controller = SimulatorController()
        self.server_factory = ServerProtocolFactory(self.on_connection,
                self.on_received)
        
        reactor.listenTCP(1079, self.server_factory)

    def start(self):
        reactor.run()

    def on_connection(self, connection):
        print "New Connection", connection.transport.getPeer() 
        game_data = self._get_game_data()
        connection.sendString(game_data)

    def on_received(self, data):
        data = pickle.loads(data)
        if isinstance(data, PlayBuildingCard):
            self.controller.play_building_card(data.card.name, data.player_id, data.slot)
        elif isinstance(data, PlaySpellCard):
            self.controller.play_spell_card(data.card.name, data.player_id, data.slot)
        elif isinstance(data, PlayUnitCard):
            self.controller.play_unit_card(data.card.name, data.player_id, data.location)
        elif isinstance(data, Reset):
            self.controller.clear()
        elif isinstance(data, Next):
            self.controller.next()

        self.broadcast_game()

    def broadcast_game(self):
        game_data = self._get_game_data()
        self.server_factory.broadcast(game_data)

    def _get_game_data(self):
        game = self.controller.game
        pickled_game = pickle.dumps(game)
        return pickled_game
        

if __name__ == "__main__":
    s = SimulatorServer()
    s.start()

