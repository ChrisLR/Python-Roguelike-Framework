import abc
from combat.enums import ThreatLevel


class BodyPart(object):
    @abc.abstractclassmethod
    def uid(self):
        pass

    @abc.abstractclassmethod
    def physical_abilities(self):
        pass

    @abc.abstractclassmethod
    def relative_size(self):
        pass

    @abc.abstractclassmethod
    def threat_level(self):
        pass
