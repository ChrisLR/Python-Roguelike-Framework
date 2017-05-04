import abc


class BaseWindow(object):
    """Abstract class for all windows"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractmethod
    def handle_input(self, key_events):
        pass

