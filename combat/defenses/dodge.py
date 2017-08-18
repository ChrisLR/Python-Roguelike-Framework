from combat.defenses.base import Defense
from combat.defenseresult import DefenseResult
from echo import functions


class Dodge(Defense):
    name = "Dodge"
    description = "You dodge your opponent."
    attacker_message = "but you dodge {defender_his} attack!"
    observer_message = "but {defender_he} dodges {attacker_his} attack!"

    @classmethod
    def evaluate(cls, attack_result):
        minimum_ac = 10
        maximum_ac = minimum_ac + attack_result.target_object.get_effective_dex_modifier()

        if minimum_ac <= attack_result.total_hit_roll <= maximum_ac:
            return True
        return False

    @classmethod
    def execute(cls, attack_result):
        return DefenseResult(message=cls.get_message(attack_result))

    @classmethod
    def get_message(cls, attack_result):
        if attack_result.attacker.is_player:
            return cls.attacker_message.format(
                defender_his=functions.his_her_it(attack_result.target_object)
            )
        else:
            return cls.observer_message.format(
                attacker_his=functions.his_her_it(attack_result.attacker),
                defender=functions.he_her_it(attack_result.target_object)
            )
