import random

from combat.defenseresult import DefenseResult
from combat.defenses.base import Defense
from echo import functions


class Parry(Defense):
    name = "Parry"
    description = "You parry your opponent."
    attacker_message = "but you parry with your {defender_weapon}!"
    observer_message = "but {defender} {parries} with {defender_his} {defender_weapon}!"

    @classmethod
    def evaluate(cls, attack_result):
        defender_equipment = attack_result.context.defender.equipment
        if defender_equipment:
            if not defender_equipment.get_wielded_items():
                return False

        minimum_ac = 10
        maximum_ac = minimum_ac + attack_result.context.defender.get_effective_dex_modifier()

        if minimum_ac <= attack_result.total_hit_roll <= maximum_ac:
            return True
        return False

    @classmethod
    def execute(cls, attack_result):
        return DefenseResult(message=cls.get_message(attack_result))

    @classmethod
    def get_message(cls, attack_result):
        wielded_items = attack_result.defender.equipment.get_wielded_items()
        parry_weapon = random.choice(wielded_items)
        if attack_result.context.attacker.is_player:
            return cls.attacker_message.format(
                defender_weapon=functions.get_name_or_string(parry_weapon)
            )
        else:
            return cls.observer_message.format(
                defender=functions.he_her_it(attack_result.defender),
                defender_his=functions.his_her_it(attack_result.defender),
                defender_weapon=functions.get_name_or_string(parry_weapon),
                parries="parries" if not attack_result.defender.is_player else "parry"
            )
