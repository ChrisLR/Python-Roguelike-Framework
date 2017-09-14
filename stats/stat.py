import math
from enum import Enum


class HealthModifier(object):
    def __init__(self, value, modifier_type):
        self.value = value
        self.modifier_type = modifier_type


class StatModifier(object):
    def __init__(self, stat_enum, value, modifier_type):
        self.stat_enum = stat_enum
        self.value = value
        self.modifier_type = modifier_type

    def __int__(self):
        return self.value

    def __radd__(self, other):
        if other == 0:
            return self.value
        else:
            return self.value + other


class StatModifierType(Enum):
    Racial = "Racial"


class Stat(object):
    __slots__ = ["value", "modifier"]

    def __init__(self, value):
        self.value = value
        self.modifier = math.floor((value - 10) / 2)



