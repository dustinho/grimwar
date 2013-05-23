from Tkinter import *

from TKSimulatorScreen import *
from SimulatorActions import *
from twisted.internet import reactor, tksupport, protocol
from twisted.internet.endpoints import TCP4ClientEndpoint

import sys
sys.path.append('../')
sys.path.append('../TK_UIv2/')

from TKGameBoard import *
from PlayerProtocol import *
from Card import Card

from TKUnit import *
from TKSpell import *
from TKCardInstance import *

from Const import *

class TKSimulator:
    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, { "height": 700, "width": 1450 })
        self.canvas.grid(column = 0, row = 0, sticky=(N, W))
        self.game_board = None
        self.actions = None
        self.simulator_screen = None

        point = TCP4ClientEndpoint(reactor, "localhost", 1079)
        d = point.connect(PlayerProtocolFactory(self.update_game))
        d.addCallback(self.got_protocol)

        tksupport.install(self.window)
        reactor.run()

    def got_protocol(self, p):
        self.actions = SimulatorActions(p)

    def update_game(self, pickled_game):
        print "updated"
        try:
            game = pickle.loads(pickled_game)
        except:
            print "error unpickling game"
            return

        casting_hexes_dict = {}
        for p_id in game.players.iterkeys():
            casting_hexes_dict[p_id] = game.board.get_valid_casting_hexes(game.players[p_id])

        self.update_board(game.board)
        self.update_simulator(Card.get_all_cards_list(), casting_hexes_dict)

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
            if unit.direction == Const.FACING_LEFT:
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

    def update_simulator(self, cards, casting_hexes_dict):
        if self.simulator_screen == None:
            self.simulator_screen = self.create_simulator_screen()
        else:
            self.simulator_screen.clear()

        self.simulator_screen.paint(cards, casting_hexes_dict)

    def create_game_board(self, width, height):
        return TKGameBoard(self.canvas, (3, 3), width, height)

    def create_simulator_screen(self):
        return TKSimulatorScreen(self.actions, self.canvas, self.game_board,
                3, 30 + self.game_board.get_pixel_height())

if __name__ == "__main__":
    TKSimulator()
