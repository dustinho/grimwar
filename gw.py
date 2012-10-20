#!/usr/bin/python

import json
import random
import sys

BOARD_WIDTH = 7
BOARD_HEIGHT = 4
BOARD = {}

P0_HP = 20;
P1_HP = 20;

def main():
    print_startinfo()
    BOARD[1] = 2;
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

        cleanup_phase()

    sys.exit()

def setup_phase():
    # Set up the board
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            # Odd rows are one less in height
            if x % 2 == 1 and y == BOARD_HEIGHT - 1:
                continue
            BOARD[(x,y)] = None
    return

def place_phase(player):
    return

def move_phase(player):
    return

def damage_phase(player):
    return

def cleanup_phase():
    return

def calculate_advantage():
    return 0

def print_startinfo():
    startinfo = {
        "board_width" : BOARD_WIDTH,
        "board_height" : BOARD_HEIGHT,
    }
    print json.dumps(startinfo)
    return

if __name__ == "__main__":
    main()

