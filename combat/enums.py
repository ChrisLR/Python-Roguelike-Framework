from enum import Enum


class DamageType(Enum):
    Blunt = 0
    Slash = 1
    Pierce = 2


class ThreatLevel(Enum):
    Minor = 0
    Major = 1
    Critical = 2
    Fatal = 3
