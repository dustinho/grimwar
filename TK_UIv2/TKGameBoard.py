
import math
from Tkinter import *
from UITools import BoardTools, BoardTestTools
from TKUnit import *

RADIUS = 32
SPELL_SLOT_ROW = 1
BUILDING_SLOT_ROW = 0

class TKGameBoard:
    def __init__(self, canvas, width, height, xoffset, yoffset, radius = RADIUS):
        self.canvas = canvas

        self.major = width
        self.minor = height

        self.xoffset = xoffset
        self.yoffset = yoffset

        self.hex_radius = radius
        self.units = []

    def paint_board(self, sector_function):

        for i in xrange(self.major):
            for j in xrange(self.minor):
                if j % 2 == 1 and i == self.major - 1:
                    continue

                bp = BoardTools.get_backend_position_from_visual_position(
                        i, j, self.minor)

                sector = sector_function((bp[0], bp[1]))
                hex_options = self.get_hexagon_options(sector)

                pixel = self.get_center_pixel_from_visual_position(i, j)
                BoardTools.draw_vertical_hexagon(self.canvas, pixel[0], pixel[1], \
                        self.hex_radius, hex_options, self.get_hex_offsets)

                BoardTestTools.draw_backend_coordinates(self.canvas, i, j, pixel[0], pixel[1], \
                        self.hex_radius, self.minor)

        
        for p in xrange(2):
            for x in xrange(self.minor):
                for y in xrange(2):
                    pixel = self.get_center_pixel_for_slot(p, x, y)
                    BoardTools.draw_rect(self.canvas, pixel[0], pixel[1], \
                            hex_options, self.get_rect_offsets)


    def clear_units_from_board(self):
        for u in self.units:
            u.clear(self.canvas)
        self.units = []

    def paint_unit_on_backend_position(self, x, y, unit):
        vp = BoardTools.get_visual_position_from_backend_position(x, y, self.minor)
        self.paint_unit_on_visual_position(vp[0], vp[1], unit) 

    def paint_unit_on_visual_position(self, x, y, unit):
        pixel = self.get_center_pixel_from_visual_position(x, y)
        unit.paint(self.canvas, pixel[0], pixel[1] )  
        self.units.append(unit)

    def paint_spell_on_slot(self, player_id, slot, spell):
        pixel = self.get_center_pixel_for_slot(player_id, slot, SPELL_SLOT_ROW)
        spell.paint(self.canvas, pixel[0], pixel[1] )
        self.units.append(spell)

    def paint_building_on_slot(self, player_id, slot, building):
        pixel = self.get_center_pixel_for_slot(player_id, slot, BUILDING_SLOT_ROW)
        building.paint(self.canvas, pixel[0], pixel[1])
        self.units.append(building)

    def get_center_pixel_from_visual_position(self, x, y):
        offsets = self.get_hex_offsets()
        xoffset = offsets[0]
        yoffset = offsets[1]

        shifts = self.get_hex_shifts()
        xshift = shifts[0]
        yshift = shifts[1]

        oddOffset = 0
        if y % 2 == 1:
            oddOffset = xoffset

        x_pixel = self.xoffset + xoffset + oddOffset + (x * xshift)
        y_pixel = self.yoffset + self.hex_radius + (y * yshift)
        return (x_pixel, y_pixel)

    def get_center_pixel_for_slot(self, player, x, y):
        rect_offsets = self.get_rect_offsets()
        x_offset = rect_offsets[0]
        y_offset = rect_offsets[1]

        x_pix = self.xoffset + x_offset + (x + (player * (1 + self.minor))) * 2 * x_offset 
        y_pix = self.get_main_board_height() + y_offset + y * 2 * y_offset
        return (x_pix, y_pix)


    def get_hex_shifts(self):
        offsets = self.get_hex_offsets()
        xoffset = offsets[0]
        yoffset = offsets[1]

        xshift = xoffset * 2
        yshift = yoffset * 3
        return (xshift, yshift)

    def get_hex_offsets(self):
        xoffset = self.hex_radius * math.sqrt(3) / 2.0
        yoffset = self.hex_radius / 2.0
        return (xoffset, yoffset)

    def get_hexagon_options(self, sector):
        options = {"fill": "grey", "outline": "black"}
        if sector == 0:
            options["fill"] = "#666666"
        elif sector == 1:
            options["fill"] = "#555555"
        elif sector == 2:
            options["fill"] = "#444444"
        elif sector == 3:
            options["fill"] = "#555555"
        elif sector == 4:
            options["fill"] = "#666666"
            
        return options

    def get_rect_offsets(self):
        xoffset = self.hex_radius * math.sqrt(3) / 2.0
        yoffset = xoffset
        return (xoffset, yoffset)

    def get_main_board_height(self):
        yshift = self.get_hex_shifts()[1]
        height = (2 * self.hex_radius) + self.minor * yshift
        #height = self.y_offset + (2 * self.hex_radius) + self.minor * yshift
        return height

    def get_slots_height(self):
        yshift = self.get_rect_offsets()[1]
        return 3 * (2 * yshift)

    def get_pixel_height(self):
        return self.get_main_board_height() + self.get_slots_height() 

if __name__ == "__main__":
    window = Tk()
    canvas = Canvas(window, { "height": 900, "width": 1200 })
    canvas.grid(column = 0, row = 0, sticky=(N, W))
    gb = TKGameBoard(canvas, 12, 3, 3, 3, RADIUS)
    gb.paint_board(lambda x: 1) 
    tku = TKUnit("Eric", 1, 1, "^", "RED")
    gb.paint_unit_on_visual_position(0,0, tku)
    def clicked(event):
        gb.clear_units_from_board()
    canvas.bind("<Button-1>", clicked)
    window.mainloop()
