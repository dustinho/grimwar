from Player import *
from Unit import *
import logging

# Right now, Board isn't really a class, but a container data structure.
class Board:
    r"""A Board is essentially a map from coordinate pairs to Unit objects.

    More specifically, a board is a hex grid with a major axis called
    "field_length" and a minor axis called "field_width".

    It is addressed by a pair of unit vectors which generate the space:

    - (1, 0) is the unit vector one hex right ->
    - (0, 1) is the unit vector one hex up and right /`

    Some example points on a "12 by 5" board are shown below.

     /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\
    |e |  |  |  |  |  |  |  |  |  |  |f |
     \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/
     |  |  |  |  |  |  |  |  |  |  |  |
     /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\
    |b |  |  |  |  |  |  |  |  |  |  |  |
     \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/
     |d |  |  |  |  |  |  |  |  |  |  |
     /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\
    |a |c |  |  |  |  |  |  |  |  |  |  |
     \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/

    a = (0, 0)
    b = (-1, 2)
    c = (1, 0)
    d = (0, 1)
    e = (-2, 4)
    f = (9, 4)

    A Board currently contains three pieces of data:
    field_length: the span of the field on the unit vector (1, 0)
    field_width: the width of the field on the unit vector (0, 1)
    """

    """
    SECTOR specifies the first column (old style - a is column 0, c is columned
    2) in which a worker is considered eligible for a payout. Workers are only
    eligible for one payout from each zone.

    Sectors "face" the middle. This is best represented with old-style columns.
    Note that past the middle, sectors cols are odd.
    """
    SECTOR_COLS = [0, 6, 14, 23, 31]

    SECTOR_PAYOUT = {
        0 : 0,
        1 : 10,
        2 : 20,
        3 : 30,
        4 : 40,
    }

    def __init__(self, game, field_length=17, field_width=5):
        self.game = game
        self.field_length = field_length
        self.field_width = field_width
        self.grid = {}
        self.spells = { 0: [None] * 5, 1: [None] * 5 }
        self.buildings = { 0: [None] * 5, 1: [None] * 5 }

    def clear(self):
        self.grid = {}

    def __str__(self):
        """return a string describing all of the objects on the board"""
        return "<Board object containing ({0})>".format(
            ", ".join(["{0} at ({1},{2})".format(instance, position[0],position[1]) for (position, instance) in self.grid.iteritems()])
                )

    def refresh_units(self):
        for unit in self.grid.itervalues():
            unit.ready()
            unit.refresh_moves()

    def do_all_movements_and_combat(self, player1, player2):
        """Performs the movement and combat phases for both players

        Player1's units move, then a combat phase happens.
        Next, player2's units move, and then a second combat phase happens.
        """

        assert isinstance(player1, Player), "player {0} is not a Player".format(player1)
        assert isinstance(player2, Player), "player {0} is not a Player".format(player2)

        # Collect all the units that are owned by the specified player
        player1_items = self._positioned_units_for_player(player1)
        player2_items = self._positioned_units_for_player(player2)

        p1_moving = True
        while(p1_moving):
            p1_moving = self.do_player_movement(player1, player1_items)
            self.do_all_attacks()

        p2_moving = True
        while(p2_moving):
            p2_moving = self.do_player_movement(player2, player2_items)
            self.do_all_attacks()


    def do_player_movement(self, player, items):
        """
        Units closest to the opponent move first.
        Units move their movement speed if possible, but if not, they move as
        many spaces as they can.  So if a speed 2 unit is behind a speed 1 unit,
        both will advance one square each tick.
        """

        direction = player.get_direction()
        items.sort(key=lambda x: x[0][0], reverse=(direction == Player.FACING_RIGHT))

        direction_multiplier = (1 if direction == Player.FACING_RIGHT else -1)
        moved = False
        for position, instance in items:
            if instance.is_ready() and instance.get_remaining_moves() > 0:
                moved = self.move_instance_one_space(instance, position, direction_multiplier) \
                        or moved
        return moved

    def move_instance_one_space(self, instance, position, direction_multiplier):
        used_moves = instance.get_used_moves()
        current_position = (position[0] + (direction_multiplier * used_moves),
                position[1]) 

        delta = 1
        logging.debug("trying to move {0} at {1}".format(instance, current_position))

        possible_destination = (current_position[0] + (delta * direction_multiplier), \
                current_position[1])
        logging.debug("testing {0}".format(possible_destination))

        if not self._is_hex_on_board(possible_destination):
            print "off board"
            logging.debug("rejected for being off the board")
            instance.use_all_moves()
            return False
        if self._which_casting_zone_owns_hex(possible_destination) != Player.INVALID_PLAYER:
            # The columns at the boards' most extreme points are
            # reserved for the player to cast new units.
            print "casting zone"
            logging.debug("rejected for being in casting zone")
            instance.use_all_moves()
            return False
        if possible_destination in self.grid:
            # You can't move through or onto occupied squares, no
            # matter how fast you are.
            print "in grid"
            logging.debug("rejected for being occupied")
            instance.use_all_moves()
            return False

        destination = possible_destination
        logging.debug("moving {0} from {1} to {2}".format(instance, current_position, destination))
        self.grid[destination] = self.grid.pop(current_position)
        instance.use_move()
        return True
            

    def do_all_attacks(self):
        for position, instance in self.grid.iteritems():
            if not instance.is_ready():
                continue
            logging.debug("Attempting attacks for {0} at {1}".format(instance, position))
            if instance.get_curr_ammo() <= 0:
                continue
            valid_targets = self.what_can_unit_at_position_hit(position)
            if len(valid_targets) == 0:
                continue
            logging.debug("{0} can hit {1}".format(instance, valid_targets))
            instance.spend_ammo()
            for target in valid_targets:
                if target not in self.grid:
                    # Damage player directly
                    player_to_damage_direction = self._which_casting_zone_owns_hex(target)
                    if player_to_damage_direction != Player.INVALID_PLAYER:
                        logging.info("{0} deals {1} damage to player {2}".format(instance, instance.get_damage(), player_to_damage_direction))
                        self.game.damage_player(player_to_damage_direction, instance.get_damage())
                else:
                    # Damage enemy unit on that hex
                    enemy = self.grid[target]
                    logging.info("{0} deals {1} damage to {2}".format(instance, instance.get_damage(), enemy))
                    enemy.take_damage(instance.get_damage())
                if instance.get_attack_type() == "single":
                    break
            instance.exhaust()

    def what_can_unit_at_position_hit(self, position):
        """Given a coordinate on the grid which hold a particular unit, return
        a list of hex coordinates that describe the enemy units that the
        particular unit could hit."""
        unit = self.grid[position]
        if unit.get_curr_ammo() <= 0:
            return []
        reachable_targets = []
        for position_delta in unit.get_attack_pattern():
            target_hex = (position[0] + position_delta[0], position[1] + position_delta[1])
            if not self._is_hex_on_board(target_hex):
                # You can't hit something off-board.
                break
            target_hex_owner = self._which_casting_zone_owns_hex(target_hex)
            if target_hex_owner != unit.owner.get_direction() and target_hex_owner != Player.INVALID_PLAYER:
                # Casting squares are valid targets and deal damage to the owning player.
                reachable_targets.append(target_hex)
                continue
            if target_hex in self.grid and self.grid[target_hex].owner != unit.owner:
                # Enemy units are valid targets too.
                reachable_targets.append(target_hex)
                continue
        return reachable_targets

    def _positioned_units_for_player(self, player):
        assert isinstance(player, Player), "player {0} is not a Player".format(player)
        player_items = []
        for position, instance in self.grid.iteritems():
            if instance.owner == player:
                player_items.append( (position, instance) )
        return player_items

    def _column_distance_from_left(self, position):
        # This uses the old coordinate system, where odd-numbered rows have
        # columns 1, 3, 5,... and even-numbered rows have columns 0, 2, 4...
        return 2 * position[0] + position[1]

    def _which_casting_zone_owns_hex(self, position):
        dist_from_left = self._column_distance_from_left(position)
        if dist_from_left == 0 or dist_from_left == 1:
            return Player.FACING_RIGHT
        if dist_from_left == 2 * (self.field_length - 1) or \
            dist_from_left == 2 * (self.field_length - 1) - 1:
            return Player.FACING_LEFT
        return Player.INVALID_PLAYER

    def _is_hex_on_board(self, position):
        dist_from_left = self._column_distance_from_left(position)
        if position[1] % 2 == 0:
            return dist_from_left >= 0 and dist_from_left <= (self.field_length - 1) * 2
        else:
            return dist_from_left >= 1 and dist_from_left <= (self.field_length - 1) * 2 - 1

    def get_sector_for_position(self, position):
        """
        Find the largest sector marker (in old-style columns) that position is
        larger than.

        Sector index increases from left to right, starting at sector 0
        """
        column = self._column_distance_from_left(position)

        for sector in reversed(range(len(self.SECTOR_COLS))):
            col = self.SECTOR_COLS[sector]
            logging.debug("position: %s col: %s target_col: %s" % (
                position,
                self._column_distance_from_left(position),
                col
            ))
            if self._column_distance_from_left(position) >= col:
                return sector
        assert False, "Should have returned a sector for {0}".format(position)

    def is_playable(self, owner, position):
        """returns True if position (u,v) is playable by owner"""
        if self._which_casting_zone_owns_hex(position) != owner.direction:
            logging.debug("Position {0} not in owner {1}'s castingzone".format(
                position,
                owner.id
            ))
            return False
        if position in self.grid:
            logging.debug("Unit already exists at {0}".format(position))
            return False
        return True

    def place_unit(self, card, owner, position):
        """Places a unit owned by owner with  based on card object
        at position (u,v)"""
        if (position in self.grid): 
            logging.debug("Unit already exists at {0}".format(position))
            return
        self.grid[position] = Unit.get_unit(card, owner)

    def get_valid_casting_hexes(self, owner):
        """returns a list of tuples describing valid plays areas for owner"""
        hexes = []
        for i in xrange(self.field_width):
            if owner.direction == Player.FACING_RIGHT:
                if i%2 == 0:
                    hexes.append((-i/2,i))
                else:
                    hexes.append((-i/2+1,i))
            elif owner.direction == Player.FACING_LEFT:
                if i%2 == 0:
                    hexes.append((self.field_length -i/2-1,i))
                else:
                    hexes.append((self.field_length -i/2-2,i))
            else:
                assert False, "{0} is not a valid Player".format(owner)
        return hexes
