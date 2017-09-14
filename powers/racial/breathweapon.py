from enum import Enum

from combat.enums import DamageType
from combat.targets import Beam, Cone
from powers.racial.base import RacialPower


class DamageTypes(Enum):
    Acid = DamageType.Acid
    Cold = DamageType.Cold
    Fire = DamageType.Fire
    Lightning = DamageType.Lightning
    Poison = DamageType.Poison


class TargetTypes(Enum):
    Cone = Cone
    Line = Beam


class BreathWeapon(RacialPower):
    uid = "breath_weapon"
    name = "Breath Weapon"

    possible_damage_types = DamageTypes
    possible_target_types = TargetTypes

    def __init__(self, breath_range, damage_type, target_type, save_stat):
        self.breath_range = breath_range
        self.damage_type = damage_type
        self.target_type = target_type
        self.save_stat = save_stat
