import abc


class ContextParameter(object):
    __metaclass__ = abc.ABCMeta
    __slots__ = ["value"]

    @abc.abstractclassmethod
    def wildcard(self):
        pass

    def __init__(self, value):
        self.value = value


class Attacker(ContextParameter):
    wildcard = "{attacker}"


class AttackerWeapon(ContextParameter):
    wildcard = "{attacker_weapon}"


class Defender(ContextParameter):
    wildcard = "{defender}"


class DefenderBodypart(ContextParameter):
    wildcard = "{defender_bodypart}"


class DefenderArmor(ContextParameter):
    wildcard = "{defender_armor}"


class DefenderWeapon(ContextParameter):
    wildcard = "{defender_weapon}"


class Actor(ContextParameter):
    wildcard = "{actor}"


class TargetItem(ContextParameter):
    wildcard = "{target_item}"
