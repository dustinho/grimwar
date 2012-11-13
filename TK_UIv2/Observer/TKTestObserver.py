import sys
sys.path.append('../')
sys.path.append('../../')
from TKGameBoard import *
from ObserverProtocol import *
from twisted.internet import reactor, tksupport, protocol
import pickle
from Game import *

from optparse import OptionParser

#Example class for a game observer
class TKTestObserver:
    def __init__(self, ip="localhost"):
        self.window = Tk()
        self.canvas = Canvas(self.window, { "height": 700, "width": 1200 })
        self.canvas.grid(column = 0, row = 0, sticky=(N, W))
        self.game_board = None

        point = TCP4ClientEndpoint(reactor, ip, 1079)
        d = point.connect(ObserverProtocolFactory(self.update_board))

        tksupport.install(self.window)
        reactor.run()

    def update_board(self, pickled_game):
        game = pickle.loads(pickled_game)
        board = game.board

        if self.game_board == None:
            self.game_board = self.create_game_board(board.field_length, board.field_width)
            self.game_board.paint_board()
        else:
            self.game_board.clear_units_from_board()
        for position, unit in board.grid.iteritems():
            tku = TKUnit(unit.card.name)
            self.game_board.paint_unit_on_backend_position(position[0], position[1], tku)

    def create_game_board(self, width, height):
        return TKGameBoard(self.canvas, width, height, 3, 3)
            
         
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ip", dest="ip")
    (options, args) = parser.parse_args()

    #bad
    if options.ip != None:
        tkto = TKTestObserver(options.ip)
    else:
        tkto = TKTestObserver()
