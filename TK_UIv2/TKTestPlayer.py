from TKGameBoard import *
from TKPlayerScreen import *
from PlayerProtocol import *
from InputProtocol import *
#from PlayerInput import *
from twisted.internet import reactor, tksupport, protocol
import pickle
import sys
sys.path.append('../')
from Game import *

class TKTestPlayer:
    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, { "height": 700, "width": 1200 })
        self.canvas.grid(column = 0, row = 0, sticky=(N, W))
        self.game_board = None
        self.input_protocol = None
        self.player_screen = None
        self.player_id = 1

        point = TCP4ClientEndpoint(reactor, "localhost", 1079)
        d = point.connect(PlayerProtocolFactory(self.update_game))
        d.addCallback(self.got_protocol)

        tksupport.install(self.window)
        reactor.run()

    def got_protocol(self, p):
        self.input_protocol = InputProtocol(p)

    def update_game(self, pickled_game):
        print "updated"
        game = pickle.loads(pickled_game)

        casting_hexes = game.board.get_valid_casting_hexes(game.players[self.player_id])

        self.update_board(game.board)
        self.update_player(game.players[self.player_id], casting_hexes)

    def update_board(self, board):
        if self.game_board == None:
            print "created gameboard"
            self.game_board = self.create_game_board(board.field_length, board.field_width)
            self.game_board.paint_board()
        else:
            self.game_board.clear_units_from_board()
        for position, unit in board.grid.iteritems():
            tku = TKUnit(unit.card.name)
            self.game_board.paint_unit_on_backend_position(position[0], position[1], tku)

    def update_player(self, player, casting_hexes):
        if self.player_screen == None:
            self.player_screen = self.create_player_screen()
        else:
            self.player_screen.clear()

        self.player_screen.paint(player, casting_hexes)
        self.player = player  

    def create_game_board(self, width, height):
        return TKGameBoard(self.canvas, width, height, 3, 3)

    def create_player_screen(self):
        return TKPlayerScreen(self.input_protocol, self.player_id,
                self.canvas, self.game_board, 
                3, 3 + self.game_board.get_pixel_height())

if __name__ == "__main__":
    tktp = TKTestPlayer()
    
        
