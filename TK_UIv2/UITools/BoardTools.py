import math

def get_hex_vertex_offsets(radius):
    xoffset = radius * math.sqrt(2) / 2.0
    yoffset = radius / 2.0
    return (xoffset, yoffset)

def get_hex_tile_offsets(radius):
    vertex_offsets = get_hex_vertex_offsets(radius)
    x_tile_offset = vertex_offsets[0] * 2
    y_tile_offset = vertex_offsets[1] * 3
    return (x_tile_offset, y_tile_offset)

#Rect tile distance is related to hex tile distance in order to easily allow
#rects to line up with hexagons
def get_rect_tile_offsets(hex_radius):
    return get_hex_tile_offsets(hex_radius)

def get_rect_vertex_offsets(hex_radius):
    tile_offsets = get_rect_tile_offsets(hex_radius)
    x_voffset = tile_offsets[0] / 2
    y_voffset = tile_offsets[1] / 2

    return (x_voffset, y_voffset)

def draw_vertical_hexagon(canvas, center_pixel, radius, options):
    centerx = center_pixel[0]
    centery = center_pixel[1]

    offsets = get_hex_vertex_offsets(radius)
    xoffset = offsets[0]
    yoffset = offsets[1]

    coords = [centerx, centery + radius, \
            centerx + xoffset, centery + yoffset, \
            centerx + xoffset, centery - yoffset, \
            centerx, centery - radius, \
            centerx - xoffset, centery - yoffset, \
            centerx - xoffset, centery + yoffset]

    return canvas.create_polygon(*coords, **options)

def draw_rect(canvas, center_pixel, radius, options):
    centerx = center_pixel[0]
    centery = center_pixel[1]

    offsets = get_rect_vertex_offsets(radius)
    xoffset = offsets[0]
    yoffset = offsets[1]

    coords = [centerx + xoffset, centery + yoffset, \
            centerx + xoffset, centery - yoffset, \
            centerx - xoffset, centery - yoffset, \
            centerx - xoffset, centery + yoffset]

    return canvas.create_polygon(*coords, **options)

def draw_text(canvas, pixel, options):
    x = pixel[0]
    y = pixel[1]
    return canvas.create_text(x, y, **options)

def get_backend_position_for_visual_position(pos, board_height):
    x = pos[0]
    y = pos[1]

    new_y = board_height - y - 1
    new_x = x - new_y // 2
    return (new_x, new_y)

def get_visual_position_for_backend_position(pos, board_height):
    x = pos[0]
    y = pos[1]

    new_y = board_height - y - 1
    new_x = x + y // 2
    return (new_x, new_y)

