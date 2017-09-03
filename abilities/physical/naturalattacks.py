from abilities.physical.base import PhysicalAbility
from util import dice


class Bite(PhysicalAbility):
    name = "Bite"
    is_passive = True
    is_stackable = False

    def __init__(self, value, damage_dice=dice.D4):
        super().__init__(value)
        self.damage_dice = damage_dice


class Claw(PhysicalAbility):
    name = "Claw"
    is_passive = True
    is_stackable = False

    def __init__(self, value, damage_dice):
        super().__init__(value)
        self.damage_dice = damage_dice


class Kick(PhysicalAbility):
    name = "Kick"
    is_passive = True
    is_stackable = False


class Punch(PhysicalAbility):
    name = "Punch"
    is_passive = True
    is_stackable = False
