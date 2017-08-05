import abc
from util.operations import intersect


class BaseControl(object):
    """Abstract class for all controls"""
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.position = 0, 0
        self.dimensions = 1, 1
        self.world_position = 0, 0

    @abc.abstractmethod
    def text(self):
        pass

    @abc.abstractmethod
    def render(self, console, active):
        pass

    @abc.abstractmethod
    def handle_input(self, key_events, mouse_events):
        pass

    def local_intersect(self, other_position, other_dimensions):
        return intersect(self.position, self.dimensions, other_position, other_dimensions)

    def world_intersect(self, other_position, other_dimensions):
        return intersect(self.world_position, self.dimensions, other_position, other_dimensions)


