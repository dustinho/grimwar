

class PlayCard:
    def __init__(self, player_id, card, location):
        self.player_id = player_id
        self.card = card
        self.location = location

class BuyCard:
    def __init__(self, player_id, card_name):
        self.player_id = player_id
        self.card_name = card_name
