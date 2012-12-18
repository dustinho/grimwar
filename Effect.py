from Player import *
from Board import *
from Unit import *
from Preds import preds

class Effect:
	"""
	Effects let you define a effect to apply in json. Game should test the
	trigger conditions for a card's effect, and if they apply, call applyEffect
	with the relevant args.
	"""
	@staticmethod
	def applyEffect(effect_name, player, opponent, instance, board, args):
		return getattr(Effect, effect_name)(
			player,
			opponent,
			instance,
			board,
			args
		)

	@staticmethod
	def draw(player, opponent, instance, board, args):
		cards_to_draw = args[0]
		for x in xrange(cards_to_draw):
			player.draw()
		return
        
        @staticmethod
        def heal_row(player, opponent, instance, board, args):
                row = instance.row
                amount = args[0]
                units = board.get_units_with_preds(preds["row"](row), 
                                                   preds["owner"](player))
                for unit in units:
                        unit.take_damage(-amount)
                return
