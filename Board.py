from Player import *

# Right now, Board isn't really a class, but a container data structure.
class Board:
    r"""A Board is essentially a map from coordinate pairs to Unit objects.

    More specifically, a board is a hex grid with a major axis called
    "field_length" and a minor axis called "field_width".  It is addressed
    first by the major axis, then by the minor axis, as follows:

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
    b = (0, 1)
    c = (2, 0)
    d = (1, 0)
    e = (0, 2)
    f = (22, 2)

    We would call the example board above a "23 by 3" board.

    You may note that the numbers follow a standard (x, y) pattern, with
    odd-numbered columns vertically offset and with one fewer row.

    A Board currently contains three pieces of data:
    field_length: the length (in hexes

    """
    def __init__(self, field_length=21, field_width=5):
        self.field_length = field_length
        self.field_width = field_width
        self.grid = {}
        pass

    def __str__(self):
        """return a string describing all of the objects on the board"""
        return "<Board object containing ({0})>".format(
            ", ".join(["{0} at ({1},{2})".format(instance, position[0],position[1]) for (position, instance) in self.grid.iteritems()])
                )

    def do_all_movements(self, player):
        """Advances all units owned by the specified player.

        Units closest to the opponent move first.
        Units move their movement speed if possible, but if not, they move as
        many spaces as they can.  So if a speed 2 unit is behind a speed 1 unit,
        both will advance one square each tick.
        """
        assert isinstance(player, Player), "player {0} is not a Player".format(player)
        direction = player.get_direction()

        # Collect all the units that are owned by the specified player
        player_items = []
        for position, instance in self.grid.iteritems():
            if instance.owner == player:
                player_items.append( (position, instance) )

        # sort by position - we want to move the instances closest to the enemy first
        player_items.sort(key=lambda x: x[0][0], reverse=(direction == Player.FACING_LEFT))
        direction_multiplier = 1 if direction == Player.FACING_RIGHT else -1
        for position, instance in player_items:
            max_delta = instance.get_speed()
            for possible_delta in reversed(range(instance.get_speed()+1)):
                possible_destination = (position[0] + (possible_delta * direction_multiplier), position[1])
                if possible_destination[0] > self.field_length - 1 or possible_destination[0] < 0:
                    # This movement would move the unit off the board.
                    continue
                if possible_destination not in self.grid:
                    print "moving {0} from {1} to {2}".format(instance, position, possible_destination)
                    self.grid[possible_destination] = self.grid.pop(position)
                    break

