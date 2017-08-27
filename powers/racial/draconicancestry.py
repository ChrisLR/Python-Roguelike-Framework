import abc
from enum import Enum

from powers.racial.base import RacialPower


class DraconicAncestry(RacialPower):
    __metaclass__ = abc.ABCMeta

    uid = "draconic_ancestry"
    name = "Draconic Ancestry"
    possible_types = DragonType

    def __init__(self, dragon_type):
        self.dragon_type = dragon_type


class DragonType(Enum):
    Black = "black"
    Blue = "blue"
    Brass = "brass"
    Bronze = "bronze"
    Copper = "copper"
    Gold = "gold"
    Green = "green"
    Red = "red"
    Silver = "silver"
    White = "white"
