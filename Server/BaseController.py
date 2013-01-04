import sys
sys.path.append('../')
from Game import Game

class BaseController:
    def __init__(self):
        self.game = Game(input_type='')

        self.game.pre_main_phases()

    #up to controller to decide what exactly this advances
    def advance(self):
        result = self.game.post_main_phases()
        if result is not None:
            return result

        self.game.pre_main_phases()

    def buy_card(self, player_id, card_name):
        player = self.game.players[player_id]
        player.buy(card_name)
        
    def play_unit_card(self, card, player_id, location):
        self.game.play_unit(card, player_id, location)

    def play_spell_card(self, card, player_id, slot):
        self.game.play_spell(card, player_id, slot)

    def play_building_card(self, card, player_id, slot):
        self.game.play_building(card, player_id, slot)

