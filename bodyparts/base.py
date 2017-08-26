import abc


class BodyPart(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def uid(self):
        pass

    @abc.abstractclassmethod
    def name(self):
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


class Head(BodyPart):
    __metaclass__ = abc.ABCMeta


class Neck(BodyPart):
    __metaclass__ = abc.ABCMeta


class Torso(BodyPart):
    __metaclass__ = abc.ABCMeta


class Arm(BodyPart):
    __metaclass__ = abc.ABCMeta


class Leg(BodyPart):
    __metaclass__ = abc.ABCMeta


class Hand(BodyPart):
    __metaclass__ = abc.ABCMeta


class Foot(BodyPart):
    __metaclass__ = abc.ABCMeta


class Eye(BodyPart):
    __metaclass__ = abc.ABCMeta


class Ear(BodyPart):
    __metaclass__ = abc.ABCMeta


class Mouth(BodyPart):
    __metaclass__ = abc.ABCMeta


class Brain(BodyPart):
    __metaclass__ = abc.ABCMeta


class Heart(BodyPart):
    __metaclass__ = abc.ABCMeta


class Lungs(BodyPart):
    __metaclass__ = abc.ABCMeta
