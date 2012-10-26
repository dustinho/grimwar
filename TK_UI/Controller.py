import sys
sys.path.append('../')
from Card import Card

class Controller:
  def __init__(self, UI, game):
    self.UI = UI  
    self.game = game
    self.current_player_id = 0
    self.phase = 0

    self.next_step()

  def next_step(self):
    if self.phase == 0:
      self.game.upkeep_phase()
      self.game.notify_listeners()
      self.phase += 1 
      self.next_step()
    elif self.phase == 1:
      self.current_player_id = 0 
      self.phase += 1
      return
    elif self.phase == 2:
      self.current_player_id = 1 
      self.phase += 1
      return
    elif self.phase == 3:
      self.do_move()
      self.game.damage_phase()
      self.game.money_phase()
      result = self.game.cleanup_phase()
      if result is not None:
        return result

      self.game.increment_turn()
      self.phase = 0
      self.next_step()
 
  def do_move(self):
      first = self.game.calculate_advantage()
      second = (first + 1) % 2
      self.game.move_phase(self.game.players[first])
      self.game.move_phase(self.game.players[second])

  def get_playable_locations(self, player_id):
    player = self.game.players[player_id]
    return self.game.board.get_valid_casting_hexes(player)

  def get_hand(self, player_id):
    return self.game.players[player_id].hand

  def get_grimoire(self, player_id):
    #Amount, Cost, Name
    l = []
    for name, count in self.game.players[player_id].grimoire.library.iteritems():
      amount = count
      card = Card.get_card(name)
      cost = card.buy_cost
      name = card.name
      l.append((amount, name, cost))
    return l

  def buy_card(self, player_id, card_name):
    player = self.game.players[player_id]
    player.buy(card_name) 

  def play_card(self, card, player_id, position):
    self.game.play_card(card, player_id, position)
    self.game.notify_listeners()
    return True

