
import math
from Tkinter import *
from UITools import BoardTools, BoardTestTools
from TKUnit import *
import ui_cfg

class TKBattlefield:
    def __init__(self, canvas, top_left_pixel, width, height):
        self.canvas = canvas

        self.major = width
        self.minor = height

        self.xoffset = top_left_pixel[0]
        self.yoffset = top_left_pixel[1]

        self.hex_radius = ui_cfg.hex_radius

    def paint(self, sector_function):
        for i in xrange(self.major):
            for j in xrange(self.minor):
                if j % 2 == 1 and i == self.major - 1:
                    continue

                visual_pos = (i, j)
                bp = BoardTools.get_backend_position_for_visual_position( \
                        visual_pos, self.minor)

                sector = sector_function(bp)
                hex_options = self._get_hexagon_options(sector)

                pixel = self.get_center_pixel_for_visual_position(visual_pos)
                BoardTools.draw_vertical_hexagon(self.canvas, pixel, \
                        self.hex_radius, hex_options)

                BoardTestTools.draw_backend_coordinates(self.canvas, \
                        visual_pos, pixel, \
                        self.hex_radius, self.minor)

    """
    def paint_unit_on_backend_position(self, pos, unit):
        vp = BoardTools.get_visual_position_for_backend_position(pos, self.minor)
        self._paint_unit_on_visual_position(vp, unit) 

    def _paint_unit_on_visual_position(self, pos, unit):
        pixel = self.get_center_pixel_for_visual_position(pos)
        unit.paint(self.canvas, pixel)  
        self.units.append(unit)
    """

    def get_center_pixel_for_visual_position(self, pos):
        rel_pixel = self._get_relative_center_pixel_for_visual_position(pos)
        return (self.xoffset + rel_pixel[0], self.yoffset + rel_pixel[1])

    def _get_relative_center_pixel_for_visual_position(self, pos):
        x = pos[0]
        y = pos[1]

        offsets = BoardTools.get_hex_vertex_offsets(self.hex_radius)
        xoffset = offsets[0]
        yoffset = offsets[1]

        shifts = BoardTools.get_hex_tile_offsets(self.hex_radius)
        xshift = shifts[0]
        yshift = shifts[1]

        oddOffset = 0
        if y % 2 == 1:
            oddOffset = xoffset

        x_pixel = xoffset + oddOffset + (x * xshift)
        y_pixel = self.hex_radius + (y * yshift)
        return (x_pixel, y_pixel)

    def _get_hexagon_options(self, sector):
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

    def get_pixel_height(self):
        tile_offsets = BoardTools.get_hex_tile_offsets(self.hex_radius)
        y_toff = tile_offsets[1]
        height = ((self.minor-1) * y_toff) + 2 * self.hex_radius
        return height

    def get_pixel_width(self):
        xshift = BoardTools.get_hex_tile_offsets(self.hex_radius)[0]
        width = self.major * xshift
        return width

if __name__ == "__main__":
    window = Tk()
    canvas = Canvas(window, { "height": 600, "width": 1350 })
    canvas.grid(column = 0, row = 0, sticky=(N, W))
    bf = TKBattlefield(canvas, (3, 3), 19, 5)
    bf.paint(lambda x: 1) 

    def clicked(event):
        print event.x, event.y
    canvas.bind("<Button-1>", clicked)
    window.mainloop()
