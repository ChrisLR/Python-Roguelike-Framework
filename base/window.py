import abc


class BaseWindow(object):
    """Abstract class for all layers"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def render(self, active):
        pass

    @abc.abstractmethod
    def handle_input(self, key_events, mouse_events):
        pass

