#!/usr/bin/python

from Player import Player
from Board import *
from Card import *
from HeroCard import *

import json
import random
import sys

BOARD_LENGTH = 31
BOARD_WIDTH = 4

class Game:
    def __init__(self):
        self.players = {}
        self.board = None

        print_startinfo()
        # input = raw_input()

        # Setup
        self.setup_game()

    def setup_game(self):
        # Set up board
        self.board = Board(field_length=BOARD_LENGTH, field_width=BOARD_WIDTH)

        # Instantiate Players/Decks
        self.players[0] = Player()
        self.players[1] = Player()
        self.players[1].set_direction(Player.FACING_LEFT)

    def do_place_phase(self, player):
        return

    def do_move_phase(self, player):
        return

    def do_damage_phase(self):
        self.board.do_all_attacks()

    def cleanup_phase(self):
        locations_to_delete = []
        for location, unit in self.board.grid.iteritems():
            if unit.get_curr_hp() <= 0:
                unit.owner.unit_died(unit)
                locations_to_delete.append(location)

        for loc in locations_to_delete:
            del self.board.grid[loc]

        # TODO Calculate Gameover
        return (self.players, self.board)

    def mainloop(self):
        # Main Loop
        while (True):
            self.do_place_phase(1)
            self.do_place_phase(2)

            first = calculate_advantage()
            second = (first + 1) % 2

            self.do_move_phase(first)
            self.do_move_phase(second)

            self.do_damage_phase()

            print_state(self.players, self.board)

            (self.players, self.board) = self.cleanup_phase()

            # Run one turn
            sys.exit()
        sys.exit()

## Debug function to print out current state
def print_state(players, board):
    for p, cm in players.items():
        print "%d card state:" % p
        print cm
    print ""
    return



def calculate_advantage():
    return 0

## Print out information needed to instantiate game
def print_startinfo():
    startinfo = {
        "board_length" : BOARD_LENGTH,
        "board_width" : BOARD_WIDTH,
    }
    print json.dumps(startinfo)
    return

if __name__ == "__main__":
    main()

