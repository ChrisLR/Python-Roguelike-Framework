import abc


class Finisher(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def name(self):
        pass

    @abc.abstractclassmethod
    def description(self):
        pass

    @abc.abstractclassmethod
    def evaluate(self, attack_result):
        pass

    @abc.abstractclassmethod
    def execute(self, attack_result):
        pass

    @abc.abstractmethod
    def attacker_message(self):
        pass

    @abc.abstractmethod
    def observer_message(self):
        pass