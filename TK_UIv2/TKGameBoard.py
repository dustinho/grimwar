
import math
from Tkinter import *
from UITools import BoardTools, BoardTestTools
from TKUnit import *

RADIUS = 32

class TKGameBoard:
    def __init__(self, canvas, width, height, xoffset, yoffset, radius = RADIUS):
        self.canvas = canvas

        self.major = width
        self.minor = height

        self.xoffset = xoffset
        self.yoffset = yoffset

        self.hex_radius = radius
        self.units = []

    def paint_board(self):
        hex_options = self.get_hexagon_options()

        for i in xrange(self.major):
            for j in xrange(self.minor):
                if j % 2 == 1 and i == self.major - 1:
                    continue
                pixel = self.get_center_pixel_from_visual_position(i, j)
                BoardTools.draw_vertical_hexagon(self.canvas, pixel[0], pixel[1], \
                        self.hex_radius, hex_options, self.get_offsets)

                BoardTestTools.draw_backend_coordinates(self.canvas, i, j, pixel[0], pixel[1], \
                        self.hex_radius, self.minor)

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

    def get_center_pixel_from_visual_position(self, x, y):
        offsets = self.get_offsets()
        xoffset = offsets[0]
        yoffset = offsets[1]

        shifts = self.get_shifts()
        xshift = shifts[0]
        yshift = shifts[1]

        oddOffset = 0
        if y % 2 == 1:
            oddOffset = xoffset

        x_pixel = self.xoffset + xoffset + oddOffset + (x * xshift)
        y_pixel = self.yoffset + self.hex_radius + (y * yshift)
        return (x_pixel, y_pixel)

    def get_shifts(self):
        offsets = self.get_offsets()
        xoffset = offsets[0]
        yoffset = offsets[1]

        xshift = xoffset * 2
        yshift = yoffset * 3
        return (xshift, yshift)

    def get_offsets(self):
        xoffset = self.hex_radius * math.sqrt(3) / 2.0
        yoffset = self.hex_radius / 2.0
        return (xoffset, yoffset)

    def get_hexagon_options(self):
        options = {"fill": "grey", "outline": "black"}
        return options

    def get_pixel_height(self):
        yshift = self.get_shifts()[1]
        height = (2 * self.hex_radius) + self.minor * yshift
        return height

if __name__ == "__main__":
    window = Tk()
    canvas = Canvas(window, { "height": 900, "width": 1200 })
    canvas.grid(column = 0, row = 0, sticky=(N, W))
    gb = TKGameBoard(canvas, 12, 3, 3, 3, RADIUS)
    gb.paint_board() 
    tku = TKUnit("Eric")
    gb.paint_unit_on_visual_position(0,0, tku)
    def clicked(event):
        gb.clear_units_from_board()
    canvas.bind("<Button-1>", clicked)
    window.mainloop()
