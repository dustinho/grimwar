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

UPKEEP_GOLD = 1

class Game:
    def __init__(self):
        self.players = {}
        self.board = None
        print_startinfo()
        self.setup_phase()

    def setup_phase(self):
        # Set up board
        self.board = Board(field_length=BOARD_LENGTH, field_width=BOARD_WIDTH)

        # Instantiate Players/Decks
        self.players[0] = Player()
        self.players[1] = Player()

    def mainloop(self):
        # Main Loop
        while (True):
            self.upkeep_phase()

            self.place_phase(1)
            self.place_phase(2)

            first = self.calculate_advantage()
            second = (first + 1) % 2

            self.move_phase(first)
            self.move_phase(second)

            # Damage happens concurrently
            self.damage_phase()

            self.money_phase()

            print_state(self.players, self.board)

            self.cleanup_phase()

            # Run one turn
            sys.exit()
        sys.exit()

    def upkeep_phase(self):
        for id, player in self.players.iteritems():
            player.gold += UPKEEP_GOLD

    def place_phase(self, player):
        return

    def move_phase(self, player):
        return

    def damage_phase(self):
        return

    def money_phase(self):
        """
        Workers get money from the sector they end up in, but should only be
        paid for a sector once per life.
        """
        for location, unit in self.board.grid.iteritems():
            if isinstance(unit, Worker):
                sector = self.board.get_sector_for_position(location)
                if sector not in unit.visited_sectors:
                    unit.owner.gold += self.board.SECTOR_PAYOUT[sector]
                    unit.visited_sectors.append(sector)

    def cleanup_phase(self):
        locations_to_delete = []
        for location, unit in self.board.grid.iteritems():
            if unit.get_curr_hp() <= 0:
                unit.owner.unit_died(unit)
                locations_to_delete.append(location)
        for loc in locations_to_delete:
            del self.board.grid[loc]
        # TODO Calculate Gameover

    def calculate_advantage(self):
        return 0

## Debug function to print out current state
def print_state(players, board):
    for p, cm in players.items():
        print "%d card state:" % p
        print cm
    print ""
    return

## Print out information needed to instantiate game
def print_startinfo():
    startinfo = {
        "board_length" : BOARD_LENGTH,
        "board_width" : BOARD_WIDTH,
    }
    print json.dumps(startinfo)
    return

