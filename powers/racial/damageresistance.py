from combat.enums import DamageType
from powers.racial.base import RacialPower


class DamageResistance(RacialPower):
    uid = "damage_resistance"
    name = "Damage Resistance"

    possible_damage_types = DamageType

    def __init__(self, damage_type):
        self.damage_type = damage_type
