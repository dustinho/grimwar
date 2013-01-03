import BoardTools

COORD_FONT = "ms serif"
def draw_backend_coordinates(canvas, visual_pos, pixel, hex_radius,
        board_height):
    backend_position = BoardTools.get_backend_position_for_visual_position(\
            visual_pos, board_height)
    coord_str = ''.join(
            [str(backend_position[0]), ", ", str(backend_position[1])])

    x_pix = pixel[0]
    y_pix = pixel[1]

    options = { "text": coord_str, "fill": "black", "font": (COORD_FONT, hex_radius // 3) }
    return canvas.create_text(x_pix, y_pix + (hex_radius * -2 // 3), **options) 
    
