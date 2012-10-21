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

PLAYER = {}
BOARD = None

def main():
    print_startinfo()
    # input = raw_input()

    # Setup
    setup_phase()

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

        print_state()

        cleanup_phase()

    sys.exit()

## Debug function to print out current state
def print_state():
    for p, cm in PLAYER.items():
        print "%d card state:" % p
        print cm
    print ""
    return

def setup_phase():
    # Set up board
    BOARD = Board(field_length=BOARD_LENGTH, field_width=BOARD_WIDTH)

    # Instantiate Players/Decks
    PLAYER[0] = Player()
    PLAYER[1] = Player()

    return

def place_phase(player):
    return

def move_phase(player):
    return

def damage_phase(player):
    return

def cleanup_phase():
    # Calculate Gameover
    sys.exit()
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

