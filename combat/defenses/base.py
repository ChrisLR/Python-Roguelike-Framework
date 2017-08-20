import abc


class Defense(object):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def description(self):
        pass

    @abc.abstractmethod
    def attacker_message(self):
        pass

    @abc.abstractmethod
    def observer_message(self):
        pass

    @abc.abstractmethod
    def evaluate(self, attack_result):
        pass

    @abc.abstractmethod
    def execute(self, attack_result):
        pass
