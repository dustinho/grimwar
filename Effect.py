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
		"""
		@param Cards to draw
		"""
		cards_to_draw = args[0]
		for x in xrange(cards_to_draw):
			player.draw()
		return

	@staticmethod
	def heal_row(player, opponent, instance, board, args):
		"""
		@param Heal amount
		"""
                row = board.get_row_for_spell(player,instance)
		amount = args[0]
		units = board.get_units_with_preds(preds["row"](row),
			preds["owner"](player))
		for unit in units:
			unit.take_damage(-amount)
			return

	@staticmethod
	def upgrade_economy(player, opponent, instance, board, args):
		"""
		Upgrades T1 workers to T2.
		If upgrade is T2, also upgrades T2 workers to T3.

		@param Upgrade level
		"""
		upgrade_level = args[0]
		if upgrade_level >= 2:
			workers_to_upgrade = len(
				[card for card in player.discard_pile if card.name == \
				"SPeasant"]
			)
			player.discard_pile = deque([
				card for card in player.discard_pile \
				if not card.name == "SPeasant"])
			for x in xrange(workers_to_upgrade):
				player.discard_pile.append(Card.get_card("UPeasant"))

		if upgrade_level >= 1:
			workers_to_upgrade = len(
				[card for card in player.discard_pile if card.name == \
				"Peasant"]
			)
			player.discard_pile = deque([
				card for card in player.discard_pile \
				if not card.name == "Peasant"])
			for x in xrange(workers_to_upgrade):
				player.discard_pile.append(Card.get_card("SPeasant"))

