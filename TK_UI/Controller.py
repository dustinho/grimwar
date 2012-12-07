from twisted.internet import reactor, tksupport, protocol
from BoardUI import UI
import sys
sys.path.append('../')
sys.path.append('../TK_UIv2')
from Card import Card
from Game import *
from PlayerInputs import PlayCard, BuyCard


class NetListenerProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print "New connection"
        self.factory.connMade()

    def sendMessage(self, msg):
        self.transport.write(msg)

    def dataReceived(self, data):
        self.factory.receivedCallback(data)
      

class NetListenerFactory(protocol.ServerFactory):
    def __init__(self, registration, receivedCallback, connMade):
        self.listeners = []
        self.receivedCallback = receivedCallback
        registration(NetListener(self))
        self.connMade = connMade

    def buildProtocol(self, addr):
        print addr
        newListener = NetListenerProtocol(self)
        self.listeners.append(newListener)
        return newListener

    def broadcast(self, msg):
        for nl in self.listeners:
            nl.sendMessage(msg)

class NetListener:
    def __init__(self, factory):
        self.factory = factory
        pass

    def state_changed(self, game_dump):
       self.factory.broadcast(game_dump)

class Controller:
    def __init__(self):
        self.game = Game(input_type='')
        self.current_player_id = 0
        self.UI = UI(BOARD_LENGTH, BOARD_WIDTH, self) 
        self.phase = 0
        self.listeners = []

        self.next_step()
        reactor.listenTCP(1079, NetListenerFactory(self.register_listener,
            self.received_callback, self.conn_made))

    def start(self):
        tksupport.install(self.UI.window)
        reactor.run()

    def next_step(self):
        if self.phase == 0:
            self.game.upkeep_phase()
            self.UI.update_state(self.game)
            self.UI.paint_player()
            self.notify_listeners()
            self.phase += 1 
            self.next_step()
        elif self.phase == 1:
            self.current_player_id = 0 
            self.phase += 1
            return
        elif self.phase == 2:
            self.current_player_id = 1 
            self.phase += 1
            return
        elif self.phase == 3:
            self.game.move_phase()
            self.game.damage_phase()
            self.game.money_phase()
            result = self.game.cleanup_phase()
            if result is not None:
                return result

            self.game.increment_turn()
            self.phase = 0
            self.next_step()
     

    def get_playable_locations(self, player_id):
        player = self.game.players[player_id]
        return self.game.board.get_valid_casting_hexes(player)

    def get_hand(self, player_id):
        return self.game.players[player_id].hand

    def get_grimoire(self, player_id):
        #Amount, Cost, Name
        l = []
        for name, count in self.game.players[player_id].grimoire.library.iteritems():
            amount = count
            card = Card.get_card(name)
            cost = card.buy_cost
            name = card.name
            l.append((amount, name, cost))
        return l

    def buy_card(self, player_id, card_name):
        player = self.game.players[player_id]
        player.buy(card_name) 

    def play_card(self, card, player_id, location):
        self.game.play_card(card, player_id, location)
        return True

    def received_callback(self, pickle_data):
        data = pickle.loads(pickle_data)
        print data
        if isinstance(data, PlayCard):
            self.play_card(data.card.name, data.player_id, data.location)
        if isinstance(data, BuyCard):
            self.buy_card(data.player_id, data.card_name)

        self.notify_listeners()
        self.UI.update_state(self.game)

    def register_listener(self, listener):
        """Add listener to the list of interested objects whenever states change.

        A listener is simply an object that provides a callable state_changed()
        which takes a single positional argument containing a pickle of the
        Game."""
        self.listeners.append(listener)

    def notify_listeners(self):
        game_dump = pickle.dumps(self.game)
        for listener in self.listeners:
            listener.state_changed(game_dump)

    def conn_made(self):
        self.notify_listeners()
        self.UI.update_state(self.game)
