from BaseController import BaseController
import sys
sys.path.append('../')
sys.path.append('../TK_UIv2/')
sys.path.append('../TK_UIv2/UITools')
from Game import Game
from UITools import BoardTools

class SimulatorController(BaseController):
    def __init__(self):
        self.game = Game(input_type='')

        self.game.upkeep_phase()

        self.game.config_flags['Use_Hands'] = False
        self.game.config_flags['Use_Gold'] = False

        self._init_simulator_casting_hexes()

    def put_card(self, card, player_id, location):
        print card
        self.game.put_in_play(card, player_id, location)

    def clear(self):
        self.game.reset()

    def next(self):
        self.advance()

    def _init_simulator_casting_hexes(self):
        sector_dict = {}
        for x in xrange(self.game.board.field_length):
            for y in xrange(self.game.board.field_width):
                if x == self.game.board.field_length - 1 and y % 2 == 1:
                    continue
                pos = BoardTools.get_backend_position_from_visual_position(x, y, self.game.board.field_width)
                sector = self.game.board.get_sector_for_position(pos)
                if sector in sector_dict:
                    sector_dict[sector].append(pos)
                else:
                    sector_dict[sector] = [pos]

        self.game.board.right_facing_casting_zones = []
        self.game.board.right_facing_casting_zones.extend(sector_dict[0])
        self.game.board.right_facing_casting_zones.extend(sector_dict[1])

        self.game.board.left_facing_casting_zones = []
        self.game.board.left_facing_casting_zones.extend(sector_dict[3])
        self.game.board.left_facing_casting_zones.extend(sector_dict[4])

