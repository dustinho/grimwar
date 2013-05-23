def pred_for_row(row):
    """
    returns a function that returns true if position
    is in row
    """
    def row_pred(position, unit_object):
        return position[1] == row
    return row_pred


def pred_for_owner(player):
    """
    returns a function that returns true if unit_object
    belongs to player
    """
    def player_pred(position, unit_object):
        return unit_object.owner_id == player.id
    return player_pred


def pred_for_hrange(hrange, start_column):
    """
    returns a function that returns true if position
    is within hrange horizontal hexes of start_column
    """
    def hrange_pred(position, unit_object):
        return abs(start_column - position[0]) <= hrange
    return hrange_pred


preds = {"row": pred_for_row,
          "owner": pred_for_owner,
          "hrange": pred_for_hrange
          }
