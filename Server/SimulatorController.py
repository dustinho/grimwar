import sys
sys.path.append('../')
sys.path.append('../TK_UIv2/')
sys.path.append('../TK_UIv2/UITools')
from Game import Game
from Card import Card
from UITools import BoardTools

class SimulatorController:
    def __init__(self):
        self.game = Game(input_type='')

        self.game.pre_main_phases()

        self._init_simulator_casting_hexes()

    def advance(self):
        result = self.game.post_main_phases()
        if result is not None:
            return result

        self.game.pre_main_phases()

    def play_unit_card(self, card_name, player_id, location):
        self.add_card_and_gold(card_name, player_id)
        self.game.play_unit(card_name, player_id, location)

    def play_spell_card(self, card_name, player_id, slot):
        self.add_card_and_gold(card_name, player_id)
        self.game.play_spell(card_name, player_id, slot)

    def play_building_card(self, card_name, player_id, slot):
        self.add_card_and_gold(card_name, player_id)
        self.game.play_building(card_name, player_id, slot)

    def clear(self):
        self.game.reset()

    def next(self):
        self.advance()

    def add_card_and_gold(self, card_name, player_id):
        card = Card.get_card(card_name)
        self.game.players[player_id].hand.append(card)
        self.game.players[player_id].gold += card.cost

    def _init_simulator_casting_hexes(self):
        sector_dict = {}
        for x in xrange(self.game.board.field_length):
            for y in xrange(self.game.board.field_width):
                if x == self.game.board.field_length - 1 and y % 2 == 1:
                    continue
                pos = BoardTools.get_backend_position_for_visual_position((x, y), self.game.board.field_width)
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

