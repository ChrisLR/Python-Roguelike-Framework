import abc


class Ability(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def name(self):
        pass

    @abc.abstractclassmethod
    def is_stackable(self):
        pass

    @abc.abstractclassmethod
    def is_passive(self):
        pass

    def trigger(self, actor):
        pass

    @abc.abstractclassmethod
    def on_gain(self, actor):
        pass

    @abc.abstractclassmethod
    def on_loss(self, actor):
        pass

    def __init__(self, value):
        self.value = value
