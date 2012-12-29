from Tkinter import *
from UITools import BoardTools
import sys
sys.path.append('../')
from Card import *

GRIMOIRE_XOFFSET = 700
STATUS_YOFFSET = 150

class TKPlayerScreen:

    def __init__(self, player_actions, player_id, canvas, game_board, xoffset, yoffset):
        self.player_actions = player_actions
        self.player_id = player_id
        self.canvas = canvas
        self.game_board = game_board
        self.xoffset = xoffset
        self.yoffset = yoffset
        
        self.screen_items = []
        #The assingment of casting hexes doesnt seems right
        self.casting_buttons = []
        self.casting_hexes = []

    def paint(self, player, casting_hexes):
        self.casting_hexes = casting_hexes
        self.paint_hand(player.hand)
        self.paint_grimoire(player.grimoire)
        self.paint_status(player)

    def clear(self):
        for item in self.screen_items:
            self.canvas.delete(item)
        self.screen_items = []

    def paint_hand(self, hand):
        def hand_button_command(card):
            return lambda: self.card_clicked(card)

        x = self.xoffset
        y = self.yoffset

        button_offset = 130

        for card in hand:
            btn_text = ''.join( [card.name, " $", str(card.cost)] )
            card_opts = { "anchor":W, "window": Button(text=btn_text, \
                    command=hand_button_command(card)) }

            button = self.canvas.create_window(x, y, **card_opts)
            self.screen_items.append(button) 

            x += button_offset

    def card_clicked(self, card):
        self.clear_casting_buttons()

        if isinstance(card, SpellCard):
            self.paint_spell_casting_buttons(card)
        elif isinstance(card, BuildingCard):
            self.paint_building_casting_buttons(card)
        else:
            self.paint_unit_casting_buttons(card)

    def paint_unit_casting_buttons(self, card):
        def play_unit_command(pid, c, l):
            return lambda: self.play_unit_card(pid, c, l) 

        for i, loc in enumerate(self.casting_hexes):
            vp = BoardTools.get_visual_position_from_backend_position(loc[0], loc[1],
                    self.game_board.minor)
            pix = self.game_board.get_center_pixel_from_visual_position(vp[0], vp[1])

            btn = Button(text=str(i),
                    command=play_unit_command(self.player_id, card, loc))
            btn_opts = { "window": btn }
            self.casting_buttons.append(self.canvas.create_window(pix[0], pix[1], **btn_opts))
             
    def paint_spell_casting_buttons(self, card):
        def play_spell_command(pid, c, s):
            return lambda: self.play_spell_card(pid, c, s)

        for i in xrange(self.game_board.minor):
            pix = self.game_board.get_center_pixel_for_slot(self.player_id, i, 1)
            btn = Button(text=str(i),
                    command=play_spell_command(self.player_id, card, i))
            btn_opts = { "window": btn }
            self.casting_buttons.append(self.canvas.create_window(pix[0], pix[1], **btn_opts))

    def paint_building_casting_buttons(self, card):
        def play_building_command(pid, c, s):
            return lambda: self.play_building_card(pid, c, s)

        for i in xrange(self.game_board.minor):
            pix = self.game_board.get_center_pixel_for_slot(self.player_id, i, 0)
            btn = Button(text=str(i),
                    command= play_building_command(self.player_id, card, i))
            btn_opts = { "window": btn }
            self.casting_buttons.append(self.canvas.create_window(pix[0], pix[1], **btn_opts))

    #this indirection is necessary due to the way closure works
    #in other words, removing the middle step sets these variables equal to
    #last value of the iteration
    def play_unit_card(self, player_id, card, location):
        self.clear_casting_buttons()
        self.player_actions.play_unit_card(player_id, card, location)

    def play_spell_card(self, player_id, card, slot):
        self.clear_casting_buttons()
        self.player_actions.play_spell_card(player_id, card, slot)

    def play_building_card(self, player_id, card, slot):
        self.clear_casting_buttons()
        self.player_actions.play_building_card(player_id, card, slot)

    def clear_casting_buttons(self):
        for casting_button in self.casting_buttons:
            self.canvas.delete(casting_button)

    def paint_grimoire(self, grimoire): 
        def buy_card_command(card_name):
            return lambda: self.buy_card(card_name)

        x = self.xoffset + GRIMOIRE_XOFFSET
        y = self.yoffset

        y_change = 25

        for name, count in grimoire.library.iteritems():
            amount = count
            #FIXME: Shouldn't need the dependency on card
            card = Card.get_card(name)
            cost = card.buy_cost
            name = card.name

            btn_text = ''.join([str(amount), 'x ', name, ' $', str(cost)]) 
            btn_opts = { "anchor": W, "window": Button(text=btn_text, \
                    command=buy_card_command(name)) }

            btn = self.canvas.create_window(x, y, **btn_opts)
            self.screen_items.append(btn)
            y += y_change

    def buy_card(self, card_name):
        print card_name
        self.player_actions.buy_card(self.player_id, card_name)

    def paint_status(self, player):
        x = self.xoffset
        y = self.yoffset + STATUS_YOFFSET

        lbl = Label(text=''.join(['Player: ', str(self.player_id), '\n', 
                str(player)]), justify=LEFT)
        lbl_opts = { "window": lbl, "anchor": NW }
        self.screen_items.append(self.canvas.create_window(x, y, **lbl_opts))

