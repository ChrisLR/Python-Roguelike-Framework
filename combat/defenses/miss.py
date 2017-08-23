from combat.defenseresult import DefenseResult
from combat.defenses.base import Defense
from echo import functions


class Miss(Defense):
    name = "Miss"
    description = "The opponent missed."
    attacker_message = "but you miss {defender_him}!"
    observer_message = "but {attacker_he} misses {defender}!"

    @classmethod
    def evaluate(cls, attack_result):
        if attack_result.total_hit_roll <= 10:
            return True
        return False

    @classmethod
    def execute(cls, attack_result):
        return DefenseResult(message=cls.get_message(attack_result))

    @classmethod
    def get_message(cls, attack_result):
        attacker = attack_result.context.attacker
        defender = attack_result.context.defender
        if attacker.is_player:
            return cls.attacker_message.format(
                defender_him=functions.him_her_it(defender)
            )
        else:
            return cls.observer_message.format(
                attacker_he=functions.he_her_it(attacker),
                defender=functions.name_or_you(defender)
            )
