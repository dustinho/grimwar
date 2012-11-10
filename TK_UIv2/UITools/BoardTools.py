
def draw_vertical_hexagon(canvas, centerx, centery, radius, options, offsetFunction):
    offsets = offsetFunction()
    xoffset = offsets[0]
    yoffset = offsets[1]

    coords = [centerx, centery + radius, \
            centerx + xoffset, centery + yoffset, \
            centerx + xoffset, centery - yoffset, \
            centerx, centery - radius, \
            centerx - xoffset, centery - yoffset, \
            centerx - xoffset, centery + yoffset]

    return canvas.create_polygon(*coords, **options)

def draw_text(canvas, x, y, options):
    return canvas.create_text(x, y, **options)

def get_backend_position_from_visual_position(x, y, board_height):
    new_y = board_height - y - 1
    new_x = x - new_y // 2
    return (new_x, new_y)

def get_visual_position_from_backend_position(x, y, board_height):
    new_y = board_height - y - 1
    new_x = x + y // 2
    return (new_x, new_y)
