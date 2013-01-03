
import ui_cfg
from TKBattlefield import TKBattlefield
from TKPlayerBase import TKPlayerBase

from UITools import BoardTools

from TKUnit import TKUnit
from TKCardInstance import TKCardInstance

class TKGameBoard:
    def __init__(self, canvas, top_left_pixel, bf_width, bf_height):
        self.canvas = canvas

        self.xoffset = top_left_pixel[0]
        self.yoffset = top_left_pixel[1]

        self.bf_width = bf_width
        self.bf_height = bf_height

        self.hex_radius = ui_cfg.hex_radius
        self.spacing = -self.hex_radius // 2

        self.card_instances = []
        self.bases = {}

        base0x = self.xoffset
        base0y = self.yoffset
        self.bases[0] = TKPlayerBase(self.canvas, (base0x, base0y), bf_height,
                TKPlayerBase.LEFT)

        bfx = base0x + self.bases[0].get_pixel_width() + self.spacing 
        bfy = base0y
        self.battlefield = TKBattlefield(self.canvas, (bfx, bfy), bf_width,
                bf_height)

        base1x = bfx + self.battlefield.get_pixel_width() + self.spacing
        base1y = base0y
        self.bases[1] = TKPlayerBase(self.canvas, (base1x, base1y), bf_height,
                TKPlayerBase.RIGHT)
        
    def paint(self, fn_battlefield_sector):
        self.bases[0].paint()
        self.battlefield.paint(fn_battlefield_sector)
        self.bases[1].paint()

    def paint_unit_on_battlefield(self, pos, unit):
        pixel = self.get_center_pixel_for_battlefield_position(pos)
        unit.paint(self.canvas, pixel)
        self.card_instances.append(unit)

    def paint_spell_in_base(self, player_id, slot_num, spell_instance):
        self._paint_instance_in_base(player_id, 
                (TKPlayerBase.SPELL_COLUMN_INDEX, slot_num),
                spell_instance)

    def paint_building_in_base(self, player_id, slot_num, building_instance):
        self._paint_instance_in_base(player_id, 
                (TKPlayerBase.BUILDING_COLUMN_INDEX, slot_num),
                building_instance)

    def _paint_instance_in_base(self, player_id, slot, instance):
        pixel = self.get_center_pixel_for_player_base_slot(player_id, slot)
        instance.paint(self.canvas, pixel)
        self.card_instances.append(instance)

    def clear(self):
        for instance in self.card_instances:
            instance.clear(self.canvas)
        self.card_instances = []

    def get_pixel_height(self):
        return max(self.battlefield.get_pixel_height(), \
                self.bases[0].get_pixel_height(), \
                self.bases[1].get_pixel_height())

    def get_pixel_width(self):
        return self.bases[0].get_pixel_width() + \
                self.battlefield.get_pixel_width() + \
                self.bases[1].get_pixel_width() + (2 * self.spacing)

    def get_center_pixel_for_battlefield_position(self, pos):
        vp = BoardTools.get_visual_position_for_backend_position(pos, \
                self.bf_height)
        pixel = self.battlefield.get_center_pixel_for_visual_position(vp)
        return pixel

    def get_center_pixel_for_player_base_slot(self, player_id, slot):
        pixel = self.bases[player_id].get_center_pixel_for_slot(slot)
        return pixel

if __name__ == "__main__":
    from Tkinter import *
    window = Tk()
    canvas = Canvas(window, { "height": 400, "width": 1450 })
    canvas.grid(column = 0, row = 0, sticky = (N,W))

    board = TKGameBoard(canvas, (3, 3), 18, 5)
    board.paint(lambda x: 1)

    tku = TKUnit('Eric', 5, 5, '^', "CYAN")
    board.paint_unit_on_battlefield((0,0), tku)

    tkci1 = TKCardInstance('Spell1')
    board.paint_spell_in_base(0, 1, tkci1)

    tkci2 = TKCardInstance('Build1')
    board.paint_spell_in_base(1, 4, tkci2)
    print board.get_pixel_height()
    print board.get_pixel_width()
    def clicked(event):
        board.clear()
        print event.x, event.y

    canvas.bind("<Button-1>", clicked)
    window.mainloop()
    
