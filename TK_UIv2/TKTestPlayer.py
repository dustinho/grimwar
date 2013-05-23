from TKGameBoard import *
from TKUnit import *
from TKSpell import *
from TKCardInstance import *
from Tkinter import *

from TKPlayerScreen import *
from PlayerProtocol import *
from PlayerActions import *
from twisted.internet import reactor, tksupport, protocol
from twisted.internet.endpoints import TCP4ClientEndpoint

import pickle
import sys
sys.path.append('../')
from Game import *
from Const import *

from optparse import OptionParser

class TKTestPlayer:
    def __init__(self, ip, player_id):
        self.window = Tk()
        self.canvas = Canvas(self.window, { "height": 900, "width": 1450 })
        self.canvas.grid(column = 0, row = 0, sticky=(N, W))
        self.game_board = None
        self.player_actions = None
        self.player_screen = None
        self.player_id = player_id

        point = TCP4ClientEndpoint(reactor, ip, 1079)
        d = point.connect(PlayerProtocolFactory(self.update_game))
        d.addCallback(self.got_protocol)

        tksupport.install(self.window)
        reactor.run()

    def got_protocol(self, p):
        self.player_actions = PlayerActions(p)

    def update_game(self, pickled_game):
        print "updated"
        try:
            game = pickle.loads(pickled_game)
        except:
            print "error unpickling game"
            return

        casting_hexes = game.board.get_valid_casting_hexes(game.players[self.player_id])

        self.update_board(game.board)
        self.update_player(game.players[self.player_id], casting_hexes)

    def update_board(self, board):
        if self.game_board == None:
            print "created gameboard"
            self.game_board = self.create_game_board(board.field_length, board.field_width)
            self.game_board.paint(board.get_sector_for_position)
        else:
            self.game_board.clear()

        for position, unit in board.grid.iteritems():
            direction = ">"
            color = "RED"
            if unit.owner.direction == Const.FACING_LEFT:
                direction = "<"
                color = "BLUE"
            tku = TKUnit(unit.card.name, unit.get_damage(),
                    unit.get_curr_ammo(), unit.get_curr_hp(),
                    direction, color)
            self.game_board.paint_unit_on_battlefield(position, tku)

        for player_id, spell_list in board.spells.iteritems():
            for slot_num, spell in enumerate(spell_list):
                if spell:
                    tks = TKSpell(spell.card.name, spell.cast_time_remaining, "BLACK")
                    self.game_board.paint_spell_in_base(player_id, slot_num, tks)

        for player_id, building_list in board.buildings.iteritems():
            for slot_num, building in enumerate(building_list):
                if building:
                    tkci = TKCardInstance(building.card.name)
                    self.game_board.paint_building_in_base(player_id, slot_num, tkci)

    def update_player(self, player, casting_hexes):
        if self.player_screen == None:
            self.player_screen = self.create_player_screen()
        else:
            self.player_screen.clear()

        self.player_screen.paint(player, casting_hexes)
        self.player = player

    def create_game_board(self, width, height):
        return TKGameBoard(self.canvas, (3, 3), width, height)

    def create_player_screen(self):
        return TKPlayerScreen(self.player_actions, self.player_id,
                self.canvas, self.game_board,
                3, 30 + self.game_board.get_pixel_height())

if __name__ == "__main__":
    #bad code
    #hack
    parser = OptionParser()
    parser.add_option("-n", "--player_id", dest="player_id")
    parser.add_option("-i", "--ip", dest="ip")
    (options, args) = parser.parse_args()

    tktp = TKTestPlayer(options.ip, int(options.player_id))

