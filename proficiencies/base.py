import abc


class Proficiency(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def uid(self):
        pass

    @abc.abstractclassmethod
    def name(self):
        pass
