def intersect(position, dimensions, other_position, other_dimensions):
    x, y = position
    width, height = dimensions
    other_x, other_y = other_position
    other_width, other_height = other_dimensions
    return (x <= other_x + other_width and x + width >= other_x and
            y <= other_y + other_height and y + height >= other_y)
