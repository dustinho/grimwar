def pred_for_row(row):
    def row_pred(position, unit_object):
        return position[1] == row
    return row_pred

def pred_for_owner(player):
    def player_pred(position, unit_object):
        return unit_object.owner == player
    return player_pred

preds = { "row" : pred_for_row,
          "owner" : pred_for_owner
          }
