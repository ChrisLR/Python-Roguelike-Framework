import abc


class Language(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def uid(self):
        pass

    @abc.abstractclassmethod
    def name(self):
        pass


class Common(Language):
    uid = "common"
    name = "Common"


class Draconic(Language):
    uid = "common"
    name = "Draconic"
