from Player import *
from Board import *
from Unit import *
from Preds import preds
from Modifier import *

class EffectUtils:
    """
    EffectUtils are helper functions to ease the creation of 
    complicated Effects.
    """
    @staticmethod
    def destroy_unit(unit, board):
        """
        Destroys a unit object on board. 
        """
        location = board.get_unit_position(unit)
        unit.owner.unit_died(unit)
        del board.grid[location]

    @staticmethod
    def destroy_row(row, board):
        """
        Destroys all units in a row
        """
        units = board.get_units_with_preds(preds["row"](row))
        for unit in units:
            EffectUtils.destroy_unit(unit, board)