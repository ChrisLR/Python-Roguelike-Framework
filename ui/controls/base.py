import abc


class BaseControl(object):
    """Abstract class for all controls"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def text(self):
        pass

    @abc.abstractmethod
    def render(self, console, active):
        pass

    @abc.abstractmethod
    def handle_input(self, key_events, mouse_events):
        pass
