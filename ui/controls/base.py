import abc


class BaseControl(object):
    """Abstract class for all controls"""
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.position = 0, 0
        self.dimensions = 0, 0

    @abc.abstractmethod
    def text(self):
        pass

    @abc.abstractmethod
    def render(self, console, active):
        pass

    @abc.abstractmethod
    def handle_input(self, key_events, mouse_events):
        pass

    def intersect(self, other_position, other_dimensions):
        x, y = self.position
        width, height = self.dimensions
        other_x, other_y = other_position
        other_width, other_height = other_dimensions
        return (x <= other_x + other_width and x + width >= other_x and
                y <= other_y + other_height and y + height >= other_y)

    def set_position_before_render(self, console):
        self.position = console.getCursor()

    def set_dimension_after_render(self, console):
        x1, y1 = self.position
        x2, y2 = console.getCursor()

        self.dimensions = (x2 - x1, y2 - y1)

