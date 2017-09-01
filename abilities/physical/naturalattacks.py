from abilities.physical.base import PhysicalAbility


class Bite(PhysicalAbility):
    name = "Bite"
    is_passive = True
    is_stackable = False


class Claw(PhysicalAbility):
    name = "Claw"
    is_passive = True
    is_stackable = False

    def __init__(self, value, damage_dice):
        super().__init__(value)
        self.damage_dice = damage_dice


class Kick(PhysicalAbility):
    name = "Bite"
    is_passive = True
    is_stackable = False


class Punch(PhysicalAbility):
    name = "Bite"
    is_passive = True
    is_stackable = False
