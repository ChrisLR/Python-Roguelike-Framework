import abc


class Mutation(object):
    @abc.abstractclassmethod
    def name(self):
        pass

    @abc.abstractmethod
    def apply(self, actor):
        pass

    @abc.abstractmethod
    def revert(self, actor):
        pass
