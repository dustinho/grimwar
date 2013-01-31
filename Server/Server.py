from twisted.internet import reactor
from BaseController import BaseController
from ServerProtocol import ServerProtocolFactory
import sys
sys.path.append('../')
sys.path.append('../TK_UIv2')
from UserInputTypes import PlayBuildingCard, PlaySpellCard, PlayUnitCard, BuyCard

import pickle
import argparse
import pprint
import logging


class Server:
    def __init__(self):
        self.TIME = 5
        self.controller = BaseController()
        self.server_factory = ServerProtocolFactory(self.on_connection,
                self.on_received)

        reactor.listenTCP(1079, self.server_factory)

        self.go = False
        self.end = False
        logging.getLogger().setLevel(logging.INFO)

    def setTime(self, time):
        self.TIME = time

    def start(self):
        reactor.callLater(self.TIME, self.loop)
        reactor.run()

    def loop(self):
        if self.server_factory.getConnectionCount() >= 2:
            if self.go:
                result = self.controller.advance()
                if result != None:
                    self.go = False
                    self.end = True
                    print result
                self.broadcast_game()
            elif not self.end:
                self.go = True
        else:
            if self.go == True:
                print "Active Connections:"
                for conn in self.server_factory.connections:
                    print conn.transport.getPeer()

        reactor.callLater(self.TIME, self.loop)

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
        elif isinstance(data, BuyCard):
            self.controller.buy_card(data.player_id, data.card_name)

        self.broadcast_game()

    def broadcast_game(self):
        game_data = self._get_game_data()
        self.server_factory.broadcast(game_data)

    def _get_game_data(self):
        game = self.controller.game
        pickled_game = pickle.dumps(game)
        return pickled_game


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--t', type=float, default=2.5)
    args = parser.parse_args()

    s = Server()
    s.setTime(args.t)
    try:
        s.start()
    except Exception as ex:
        # Super Awesome Exception logging
        pprint.pprint(s.controller.game)
        raise ex

