import BoardTools

COORD_FONT = "ms serif"
def draw_backend_coordinates(canvas, visual_x, visual_y, x_pixel, y_pixel, \
        hex_radius, board_height):
    backend_position = BoardTools.get_backend_position_from_visual_position(visual_x, \
            visual_y, board_height)
    coord_str = ''.join([ str(backend_position[0]), ", ", str(backend_position[1]) ])

    options = { "text": coord_str, "fill": "black", "font": (COORD_FONT, hex_radius // 3) }
    return canvas.create_text(x_pixel, y_pixel + (hex_radius * -2 // 3), **options) 
    
