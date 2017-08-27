from enum import Enum


class DamageType(Enum):
    Blunt = "blunt"
    Slash = "slash"
    Pierce = "pierce"
    Acid = "acid"
    Cold = "cold"
    Fire = "fire"
    Lightning = "lightning"
    Poison = "poison"


class ThreatLevel(Enum):
    Minor = 0
    Major = 1
    Critical = 2
    Fatal = 3
