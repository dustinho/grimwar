import sys
sys.path.append('../')
from Game import Game

class BaseController:
    def __init__(self):
        self.game = Game(input_type='')

        self.game.upkeep_phase()

    #up to controller to decide what exactly this advances
    def advance(self):
        self.game.move_phase()
        self.game.damage_phase()
        self.game.money_phase()
        result = self.game.cleanup_phase()
        if result is not None:
            return result

        self.game.increment_turn()
        self.game.upkeep_phase()

    def buy_card(self, player_id, card_name):
        player = self.game.players[player_id]
        player.buy(card_name)
        
    def play_card(self, card, player_id, location):
        self.game.play_card(card, player_id, location)

