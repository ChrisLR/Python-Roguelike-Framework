from powers.racial.base import RacialPower


class BonusAttack(RacialPower):
    uid = "bonus_attack"
    name = "Bonus Attack"

    def __init__(self, attack):
        self.attack = attack
