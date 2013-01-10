import ui_cfg
from UITools import BoardTools, BoardTestTools

BASE_COLUMN_COUNT = 2

class TKPlayerBase:
    LEFT = 0
    RIGHT = 1

    BUILDING_COLUMN_INDEX = 0
    SPELL_COLUMN_INDEX = 1

    def __init__(self, canvas, top_left_pixel, row_count, direction = LEFT):
        self.canvas = canvas
        
        self.xoffset = top_left_pixel[0]
        self.yoffset = top_left_pixel[1]

        self.hex_radius = ui_cfg.hex_radius
        self.row_count = row_count

        self.direction = direction

    def paint(self):
        base_opts = self._get_base_options()
        for x in xrange(BASE_COLUMN_COUNT):
            for y in xrange(self.row_count):
                slot = (x, y)
                pixel = self.get_center_pixel_for_slot(slot)
                self._paint_tile(pixel)
    
    def _paint_tile(self, pixel):
        if ui_cfg.base_style == 1:
            BoardTools.draw_vertical_hexagon(self.canvas, pixel, \
                    self.hex_radius, self._get_base_options())
        elif ui_cfg.base_style == 2:
            BoardTools.draw_rect(self.canvas, pixel, \
                    self.hex_radius, self._get_base_options())

    def get_center_pixel_for_slot(self, slot):
        relative_pixel = self._get_relative_center_pixel_for_slot(slot)
        x = self.xoffset + relative_pixel[0]
        y = self.yoffset + relative_pixel[1]
        return (x,y)
        
    def _get_relative_center_pixel_for_slot(self, slot):
        column = slot[0]
        row = slot[1]

        if ui_cfg.base_style == 1:
            vertex_offsets = BoardTools.get_hex_vertex_offsets(self.hex_radius)
            x_voff = vertex_offsets[0]
            y_voff = vertex_offsets[1]
        
            tile_offsets = BoardTools.get_hex_tile_offsets(self.hex_radius)
            x_toff = tile_offsets[0]
            y_toff = tile_offsets[1]

            oddOffset = 0
            #odd rows are shifted by a half tile 
            if row % 2 == 1:
                oddOffset = x_toff / 2

            x_pixel = (x_toff / 2) + oddOffset + (column * x_toff)
            y_pixel = self.hex_radius + (row * y_toff)
            y_pixel = self.get_pixel_height() - y_pixel

            if (self.direction == TKPlayerBase.RIGHT):
                x_pixel = self.get_pixel_width() - x_pixel

            return (x_pixel, y_pixel)

        elif ui_cfg.base_style == 2:
            tile_offsets = BoardTools.get_rect_tile_offsets(self.hex_radius)
            x_toff = tile_offsets[0]
            y_toff = tile_offsets[1]

            x_pixel = (x_toff / 2) + (column * x_toff)
            y_pixel = (y_toff / 2) + row * y_toff
            y_pixel = self.get_pixel_height() - y_pixel
            return (x_pixel, y_pixel)

    def get_pixel_height(self):
        if ui_cfg.base_style == 1:
            tile_offsets = BoardTools.get_hex_tile_offsets(self.hex_radius)
            y_toff = tile_offsets[1]
            height = ((self.row_count-1) * y_toff) + 2 * self.hex_radius
            return height
        elif ui_cfg.base_style == 2:
            tile_offsets = BoardTools.get_rect_tile_offsets(self.hex_radius)
            y_toff = tile_offsets[1]
            height = (y_toff * self.row_count)
            return height

    def get_pixel_width(self):
        if ui_cfg.base_style == 1:
            tile_offsets = BoardTools.get_hex_tile_offsets(self.hex_radius)
            x_toff = tile_offsets[0]
            width = x_toff / 2 + (BASE_COLUMN_COUNT * x_toff)
            return width
        elif ui_cfg.base_style == 2:
            tile_offsets = BoardTools.get_rect_tile_offsets(self.hex_radius)
            x_toff = tile_offsets[0]
            width = (BASE_COLUMN_COUNT) * x_toff
            return width

    def _get_base_options(self):
        options = {"fill": "grey", "outline": "black"}
        return options

if __name__ == "__main__":
    from Tkinter import *
    window = Tk()
    canvas = Canvas(window, { "height": 700, "width": 500 })
    canvas.grid(column = 0, row = 0, sticky = (N,W))

    base = TKPlayerBase(canvas, (3, 3), 5, TKPlayerBase.RIGHT)
    base.paint()
    base2 = TKPlayerBase(canvas, (3 + base.get_pixel_width(), \
            3 + base.get_pixel_height()), 5) 
    base2.paint()

    window.mainloop()
