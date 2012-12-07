import sys
sys.path.append('../')
from Game import Game

class SimulatorController:
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

    def put_card(self, card, player_id, location):
        print card
        self.game.put_in_play(card, player_id, location)

    def clear(self):
        self.game.reset()

    def next(self):
        self.advance()
