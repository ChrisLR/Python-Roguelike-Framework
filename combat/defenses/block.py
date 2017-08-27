import random

from combat.defenseresult import DefenseResult
from combat.defenses.base import Defense
from echo import functions


class Block(Defense):
    name = "Block"
    description = "Your block with a shield."
    attacker_message = "but {defender_he} blocks your attack with {defender_his} {defender_shield}!"
    observer_message = "but {defender_he} blocks {attacker_his} attack with {defender_shield}!"

    @classmethod
    def evaluate(cls, attack_result):
        defender = attack_result.context.defender
        if not any((item for item in defender.equipment.get_wielded_items() if item.armor)):
            return False

        minimum_ac = 10 + defender.get_effective_dex_modifier()
        maximum_ac = minimum_ac + defender.get_shield_modifiers()

        if minimum_ac <= attack_result.total_hit_roll <= maximum_ac:
            return True
        return False

    @classmethod
    def execute(cls, attack_result):
        return DefenseResult(message=cls.get_message(attack_result))

    @classmethod
    def get_message(cls, attack_result):
        defender = attack_result.defender
        defender_shield = random.choice((item for item in defender.equipment.get_wielded_items() if item.armor))
        if attack_result.context.attacker.is_player:
            return cls.attacker_message.format(
                defender_he=functions.he_her_it(defender),
                defender_his=functions.his_her_it(defender),
                defender_shield=defender_shield.name,
            )
        else:
            return cls.observer_message.format(
                defender_he=functions.he_her_it(defender),
                attacker_his=functions.his_her_it(attack_result.context.attacker),
                defender_shield=defender_shield.name
            )
