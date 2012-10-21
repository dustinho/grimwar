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

def main():
    players = {}
    board = None

    print_startinfo()
    # input = raw_input()

    # Setup
    (players, board) = setup_phase(players, board)

    # Main Loop
    while (True):
        place_phase(1)
        place_phase(2)

        first = calculate_advantage()
        second = (first + 1) % 2

        move_phase(first)
        move_phase(second)

        damage_phase(first)
        damage_phase(second)

        print_state(players, board)

        (players, board) = cleanup_phase(players, board)

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

def setup_phase(players, board):
    # Set up board
    board = Board(field_length=BOARD_LENGTH, field_width=BOARD_WIDTH)

    # Instantiate Players/Decks
    players[0] = Player()
    players[1] = Player()

    return (players, board)

def place_phase(player):
    return

def move_phase(player):
    return

def damage_phase(player):
    return

def cleanup_phase(players, board):
    locations_to_delete = []
    for location, unit in board.grid.iteritems():
        if unit.get_curr_hp() <= 0:
            unit.owner.unit_died(unit)
            locations_to_delete.append(location)

    for loc in locations_to_delete:
        del board.grid[loc]

    # TODO Calculate Gameover
    return (players, board)

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

