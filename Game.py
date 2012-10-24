#!/usr/bin/python

from Player import Player
from Board import *
from Card import *

from Unit import *
import json
import random
import sys
import copy
import pickle

BOARD_LENGTH = 19
BOARD_WIDTH = 5
DRAW_FREQUENCY = 3
UPKEEP_GOLD = 1
MAX_HAND_SIZE = 5

class Game:
    def __init__(self, input_type=''):
        self.players = {}
        self.board = None
        print_startinfo()
        self.setup_phase()
        self.input_type = input_type
        self.turn = 0
        self.listeners = []

    def setup_phase(self):
        # Set up board
        self.board = Board(self, field_length=BOARD_LENGTH, field_width=BOARD_WIDTH)

        # Instantiate Players
        self.players[0] = Player(0)
        self.players[1] = Player(1)
        self.players[1].set_direction(Player.FACING_LEFT)

        # Initial Decks
        self.players[0].set_deck([
            Card.get_card('Knight'),
            Card.get_card('Footman'),
            Card.get_card('Peasant'),
            Card.get_card('Peasant'),
            Card.get_card('Peasant'),
        ])
        self.players[0].set_hand([
            Card.get_card('Footman'),
            Card.get_card('Footman'),
            Card.get_card('Peasant'),
            Card.get_card('Peasant'),
            Card.get_card('Peasant'),
        ])
        self.players[1].set_deck([
            Card.get_card('Knight'),
            Card.get_card('Footman'),
            Card.get_card('Peasant'),
            Card.get_card('Peasant'),
            Card.get_card('Peasant'),
        ])
        self.players[1].set_hand([
            Card.get_card('Footman'),
            Card.get_card('Footman'),
            Card.get_card('Peasant'),
            Card.get_card('Peasant'),
            Card.get_card('Peasant'),
        ])

        # Initial Heroes
        middle = (BOARD_WIDTH - 1) / 2
        self.put_in_play(Card.get_card('Arius'), 0, (-1, middle))
        self.put_in_play(Card.get_card('Arius'), 1, (BOARD_LENGTH-2, middle))

        # Initial Grimoire
        self.players[0].library = {'Peasant' : 10, 'Footman' : 10}
        self.players[1].library = {'Peasant' : 10, 'Footman' : 10}

    def main_loop(self):
        # Main Loop
        while (True):
            winner = self.main_loop_once()
            if winner is not None:
                return winner

    def main_loop_once(self):
        self.upkeep_phase()

        self.main_phase(0)
        self.main_phase(1)

        first = self.calculate_advantage()
        second = (first + 1) % 2

        self.move_phase(self.players[first])
        self.move_phase(self.players[second])

        # Damage happens concurrently
        self.damage_phase()

        self.money_phase()

        result = self.cleanup_phase()
        if result is not None:
            return result

        self.turn += 1
        self.notify_listeners()

    def upkeep_phase(self):
        if self.turn % DRAW_FREQUENCY == 0:
            for id, player in self.players.iteritems():
                if len(self.players[id].hand) < MAX_HAND_SIZE:
                    self.players[id].draw()
        for id, player in self.players.iteritems():
            player.gold += UPKEEP_GOLD

    def main_phase(self, id):
        if self.input_type != 'Console':
            return

        player = self.players[id]

        print "=== Turn {0}: Player {1}".format(self.turn, id)
        print player
        print "Board: {0}".format(self.board)

        while (True):
            input = raw_input('\nChoose: 1) Play 2) Buy. Hit Enter if done\n')

            if input == '1':
                while (True):
                    print "Choose a card to play or Enter for Done:"
                    i = 0
                    available_cards = sorted(list(set(
                        [x.name for x in player.hand]
                    )))
                    for name in available_cards:
                        print "{0}) {1}".format(i, name)
                        i += 1

                    card_choice = raw_input()
                    if card_choice == '':
                        break
                    card_choice = int(card_choice)

                    if card_choice < 0 or card_choice >= i:
                        print "\nInvalid Choice {0}\n".format(card_choice)
                        continue

                    x = int(raw_input('x-coor where you want to play: '))
                    y = int(raw_input('y-coor where you want to play: '))

                    self.play_card(available_cards[card_choice], id, (x,y))
                break
            elif input == '2':
                while (True):
                    print "Choose a card to buy:"
                    i = 0
                    available_cards = player.grimoire.get_buyable_card_names()
                    for name in available_cards:
                        print "{0}) {1}".format(i, name)
                        i += 1
                    card_choice = int(raw_input())

                    if card_choice < 0 or card_choice >= i:
                        print "\nInvalid Choice {0}\n".format(card_choice)
                        continue
                    elif input == '':
                        break
                    player.buy(available_cards[card_choice])
                break
            elif input == '':
                break
            else:
                print "Invalid Command"

        return

    def move_phase(self, player):
        self.board.do_all_movements(player)

    def damage_phase(self):
        self.board.do_all_attacks()

    def money_phase(self):
        """
        Workers get money from the sector they end up in, but should only be
        paid for a sector once per life.
        """
        for location, unit in self.board.grid.iteritems():
            if isinstance(unit, Worker):
                sector = self.board.get_sector_for_position(
                    location,
                    unit.owner.get_direction()
                )
                if sector not in unit.visited_sectors:
                    unit.owner.gold += self.board.SECTOR_PAYOUT[sector]
                    unit.visited_sectors.append(sector)

    def cleanup_phase(self):
        locations_to_delete = []
        for location, unit in self.board.grid.iteritems():
            if unit.get_curr_hp() <= 0:
                if isinstance(unit, Hero):
                    unit.owner.hero_died(unit)
                else:
                    unit.owner.unit_died(unit)
                locations_to_delete.append(location)

        for loc in locations_to_delete:
            del self.board.grid[loc]

        # Calculate Gameover
        is_tie = True
        for id, player in self.players.iteritems():
            if player.get_curr_health() > 0:
                is_tie = False

        for id, player in self.players.iteritems():
            if player.get_curr_health() <= 0:
                return 'Tie' if is_tie else (id + 1) % 2

        return None

    def calculate_advantage(self):
        return 0

    def damage_player(self, direction, damage):
        if direction == Player.FACING_RIGHT:
            self.players[0].take_damage(damage)
        elif direction == Player.FACING_LEFT:
            self.players[1].take_damage(damage)
        else:
            raise ValueError("Invalid direction")

    def play_card(self, card_name, id, position):
        """plays a card for player id from his hand at position (u,v)"""
        card = self.players[id].play(card_name)
        print id
        print position
        self.board.place_unit(card, self.players[id], position)

    def put_in_play(self, card, id, position):
        """ puts a unit into play without paying the cost """
        self.players[id].inplay.append(card)
        self.board.grid[(position)] = Unit.get_unit(card, self.players[id])

    def register_listener(self, listener):
        """Add listener to the list of interested objects whenever states change.

        A listener is simply an object that provides a callable state_changed()
        which takes a single positional argument containing a pickle of the
        Game."""
        self.listeners.append(listener)

    def notify_listeners(self):
        game_dump = pickle.dumps(self)
        for listener in self.listeners:
            listener.state_changed(game_dump)

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

