from Tkinter import *
import sys
sys.path.append('../')
from Card import *

sys.path.append('../TK_UIv2/')
from TKPlayerBase import TKPlayerBase

from UITools import BoardTools

class TKSimulatorScreen:
    def __init__(self, actions, canvas, game_board, xoffset, yoffset):
        self.actions = actions
        self.canvas = canvas
        self.game_board = game_board
        self.xoffset = xoffset
        self.yoffset = yoffset

        self.screen_items = []
        self.casting_hexes_dict = {}
        self.casting_buttons = []


    def paint(self, cards, player_id_to_casting_hexes_dict):
        self.casting_hexes_dict = player_id_to_casting_hexes_dict
        self.paint_controls()
        self.paint_cards(cards)


    def clear(self):
        for item in self.screen_items:
            self.canvas.delete(item)
        self.screen_items = []

    def paint_controls(self):
        x = self.xoffset
        y = self.yoffset
        txt1 = "Next"
        txt2 = "Reset"

        next_opts = { "anchor":W, "window": Button(text=txt1, \
                command=self.actions.next) }
        next_btn = self.canvas.create_window(x, y, **next_opts)
        self.screen_items.append(next_btn)

        reset_opts = { "anchor":W, "window": Button(text=txt2, \
                command=self.actions.reset) }
        reset_btn = self.canvas.create_window(x+140, y, **reset_opts)
        self.screen_items.append(reset_btn)
        

    def paint_cards(self, cards):
        def card_button_command(card):
            return lambda: self.card_clicked(card)

        x = self.xoffset
        y = self.yoffset + 50

        button_offset = 130

        for i, card in enumerate(cards):
            btn_text = ''.join( [card.name, " $", str(card.cost)] )
            card_opts = { "anchor":W, "window": Button(text=btn_text, \
                    command=card_button_command(card)) }

            button = self.canvas.create_window(x, y, **card_opts)
            self.screen_items.append(button) 

            if i % 7 == 6:
                y += 25
                x = self.xoffset
            else:
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

        for player_id, casting_hexes_list in self.casting_hexes_dict.iteritems():
            for i, pos in enumerate(casting_hexes_list):
                pix = self.game_board.get_center_pixel_for_battlefield_position(pos)

                btn = Button(text=str(i),
                        command=play_unit_command(player_id, card, pos))
                btn_opts = { "window": btn }
                self.casting_buttons.append(self.canvas.create_window(pix[0], pix[1], **btn_opts))

    def paint_spell_casting_buttons(self, card):
        def play_spell_command(pid, c, s):
            return lambda: self.play_spell_card(pid, c, s)

        self._paint_base_casting_buttons(card, TKPlayerBase.SPELL_COLUMN_INDEX,
                play_spell_command)

    def paint_building_casting_buttons(self, card):
        def play_building_command(pid, c, s):
            return lambda: self.play_building_card(pid, c, s)

        self._paint_base_casting_buttons(card, TKPlayerBase.BUILDING_COLUMN_INDEX,
                play_building_command)

    def _paint_base_casting_buttons(self, card, slot_column, on_click):
        for player_id in self.casting_hexes_dict.iterkeys():
            for i in xrange(self.game_board.bf_height):
                slot = (slot_column, i)
                pix = self.game_board.get_center_pixel_for_player_base_slot( \
                        player_id, slot)
                btn = Button(text=str(i), command=on_click(player_id, card, i))
                btn_opts = { "window": btn }
                self.casting_buttons.append(self.canvas.create_window(pix[0], pix[1], **btn_opts))

    #this indirection is necessary due to the way closure works
    #in other words, removing the middle step sets these variables equal to
    #last value of the iteration
    def play_unit_card(self, player_id, card, location):
        self.clear_casting_buttons()
        self.actions.play_unit_card(player_id, card, location)

    def play_spell_card(self, player_id, card, slot):
        self.clear_casting_buttons()
        self.actions.play_spell_card(player_id, card, slot)

    def play_building_card(self, player_id, card, slot):
        self.clear_casting_buttons()
        self.actions.play_building_card(player_id, card, slot)

    def clear_casting_buttons(self):
        for casting_button in self.casting_buttons:
            self.canvas.delete(casting_button)
