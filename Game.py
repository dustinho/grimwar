#!/usr/bin/python

from Player import *
from Board import *
from Card import *
from Unit import *
from Effect import *
from CLIClient import *

import json
import random
import sys
import copy
import pickle
import random
import math

import logging

BOARD_LENGTH = 19
BOARD_WIDTH = 5
DRAW_FREQUENCY = 2
UPKEEP_GOLD = 2
MAX_HAND_SIZE = 5


class Game:
    def __init__(self, input_type=''):
        self.players = {}
        self.board = None
        print_startinfo()
        self.setup_phase()
        self.input_type = input_type
        self.turn = 0
        self.turn_advantage = 0

    def reset(self):
        self.board.clear()

    def setup_phase(self):
        # Set up board
        self.board = Board(self, field_length=BOARD_LENGTH, field_width=BOARD_WIDTH)

        # Instantiate Players
        self.players[0] = Player(0)
        self.players[1] = Player(1)
        self.players[1].set_direction(Player.FACING_LEFT)

        # Initial Decks
        self.players[0].set_deck([
            Card.get_card('Rifleman'),
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
            Card.get_card('Rifleman'),
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
        self.pre_main_phases()
        self.main_phase(0)
        self.main_phase(1)
        gameover = self.post_main_phases()
        if gameover is not None:
            return gameover

    def pre_main_phases(self):
        logging.info("********************")
        logging.info("Beginning of Turn {0}".format(self.turn))
        self.upkeep_phase()
        self.cleanup_phase()
        self.draw_phase()

    def post_main_phases(self):
        self.spell_phase()
        self.damage_phase()
        self.cleanup_phase()
        self.move_phase()

        self.money_phase()

        result = self.cleanup_phase()
        if result is not None:
            return result

        logging.info("End of Turn {0}".format(self.turn))
        logging.info("********************")
        self.increment_turn()

    def increment_turn(self):
        self.turn += 1

    def upkeep_phase(self):
        self.turn_advantage = self.calculate_advantage()
        logging.info("Player {0} has advantage for this turn".format(self.turn_advantage))
        # Refresh must occur first
        self.board.refresh_units()

        # Let modifiers do updates. This must occur before effects, as a
        # effects may apply modifiers.
        # TODO: Building modifiers? Spell modifiers?
        for location, unit in self.board.grid.iteritems():
            for modifier in unit.modifiers:
                modifier.upkeepLogic(self.board)
        for id, player in self.players.iteritems():
            for modifier in player.modifiers:
                modifier.upkeepLogic(self.board)

        for id, player in self.players.iteritems():
            player.gold += UPKEEP_GOLD
        self.apply_phase_effects()


    def draw_phase(self):
        if self.turn % DRAW_FREQUENCY == 0:
            for id, player in self.players.iteritems():
                if len(self.players[id].hand) < MAX_HAND_SIZE:
                    self.players[id].draw()

    def main_phase(self, id):
        if self.input_type != 'Console':
            return

        CLIClient.main_phase(id, self)
        return

    def damage_phase(self):
        first = self.get_turn_advantage()
        second = (first + 1) % 2

        self.board.do_combat(self.players[first], self.players[second])

        # Reduce the health of every unit that is out of will by 1/3
        for location, unit in self.board.grid.iteritems():
            if unit.get_curr_ammo() <= 0:
                unit._hp -= int(math.ceil(float(unit.get_max_hp())/3.0))

    def move_phase(self):
        first = self.get_turn_advantage()
        second = (first + 1) % 2

        self.board.do_movements(self.players[first], self.players[second])

    def money_phase(self):
        """
        Workers get money from the sector they end up in, but should only be
        paid for a sector once per life.
        """
        for location, unit in self.board.grid.iteritems():
            if isinstance(unit, Worker):
                sector = self.board.get_sector_for_position(location)
                if sector not in unit.visited_sectors:
                    unit.owner.gold += self.board.SECTOR_PAYOUT[len(unit.visited_sectors)]
                    unit.visited_sectors.append(sector)

    def spell_phase(self):
        # Spell logic
        first = self.get_turn_advantage()
        second = (first + 1) % 2

        for i in xrange(len(self.board.spells[first])):
            spell = self.board.spells[first][i]
            if spell:
                spell.cast_time_remaining -= 1
                if spell.cast_time_remaining <= 0:
                    Effect.applyEffect(
                        spell.cast_effect,
                        self.players[first],
                        self.players[second],
                        spell,
                        self.board,
                        spell.cast_args
                    )
                    self.players[first].spell_remove(spell)
                    self.board.spells[first][i] = None

        for i in xrange(len(self.board.spells[second])):
            spell = self.board.spells[second][i]
            if spell:
                spell.cast_time_remaining -= 1
                if spell.cast_time_remaining <= 0:
                    Effect.applyEffect(
                        spell.cast_effect,
                        self.players[second],
                        self.players[first],
                        spell,
                        self.board,
                        spell.cast_args
                    )
                    self.players[second].spell_remove(spell)
                    self.board.spells[second][i] = None


    def cleanup_phase(self):
        num_removed = True
        while (num_removed):
            """
            We run cleanup whenever shit may be needed to be removed from
            the board. Cleanup will go through every modifier and check if it
            needs to go, then check if any units need to go. It'll keep doing
            this until no units die (meaning no modifiers will change, meaning
            we've reached a stable state)

            TODO: Building modifiers? Spell modifiers?
            """
            for location, unit in self.board.grid.iteritems():
                for modifier in unit.modifiers:
                    modifier.cleanupLogic(self.board)
            for id, player in self.players.iteritems():
                for modifier in player.modifiers:
                    modifier.cleanupLogic(self.board)

            num_removed = self.board.remove_dead()

        # Calculate Gameover
        is_tie = True
        for id, player in self.players.iteritems():
            if player.get_curr_health() > 0:
                is_tie = False

        for id, player in self.players.iteritems():
            if player.get_curr_health() <= 0:
                return 'Tie' if is_tie else (id + 1) % 2

        return None

    def get_turn_advantage(self):
        return self.turn_advantage

    def calculate_advantage(self):
        return (self.get_turn_advantage() + 1) % 2

    def damage_player(self, direction, damage):
        if direction == Player.FACING_RIGHT:
            self.players[0].take_damage(damage)
        elif direction == Player.FACING_LEFT:
            self.players[1].take_damage(damage)
        else:
            raise ValueError("Invalid direction")

    def play_unit(self, card_name, id, position):
        """plays a card for player id from his hand at position (u,v)"""
        if not self.board.is_playable(self.players[id], position):
            logging.debug("{0} not playable at {1}".format(card_name, position))
            return False

        card = self.players[id].play(card_name)
        if card == None:
            return False

        self.board.place_unit(card, self.players[id], position)
        return True

    def play_spell(self, spell_name, id, slot):
        """ Plays a spell at a given position (0-4 inclusive) for id"""
        if (self.board.spells[id][slot]):
            logging.debug("{0} not playable at {1}".format(spell_name, slot))
            return False

        card = self.players[id].play(spell_name)
        if card == None:
            return False

        self.board.place_spell(card, self.players[id], slot)
        return True

    def play_building(self, building_name, id, slot):
        """ Plays a buidling at a given position (0-4 inclusive) for id"""
        if (self.board.buildings[id][slot]):
            logging.debug("{0} not playable at {1}".format(building_name, slot))
            return
        card = self.players[id].play(building_name)
        self.board.place_building(card, self.players[id], slot)

    def put_in_play(self, card, id, position):
        """ puts a unit into play without paying the cost """
        self.board.is_playable(self.players[id], position)
        self.players[id].inplay.append(card)
        self.board.grid[(position)] = Unit.get_unit(card, self.players[id])

    def apply_phase_effects(self):
        """
        Go through each building and apply its Effect
        TODO: Should go through everything on the board and apply effects.
        TODO: Make this phase independent
        """
        first = self.get_turn_advantage()
        second = (first + 1) % 2
        self.apply_phase_effects_for_player(first, second)
        self.apply_phase_effects_for_player(second, first)

    def apply_phase_effects_for_player(self, player_id, opponent_id):
        for (index, object) in enumerate(self.board.buildings[player_id]):
            if object and object.upkeep_effect:
                Effect.applyEffect(
                    object.upkeep_effect,
                    self.players[player_id],
                    self.players[opponent_id],
                    object,
                    self.board,
                    object.upkeep_effect_args
                )


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

