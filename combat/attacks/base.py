import abc


class Attack(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def name(cls):
        pass

    @abc.abstractclassmethod
    def description(cls):
        pass

    @abc.abstractclassmethod
    def target_type(cls):
        pass

    @abc.abstractclassmethod
    def execute(cls, actor, target):
        pass
