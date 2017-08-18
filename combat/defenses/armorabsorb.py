from combat.defenseresult import DefenseResult
from combat.defenses.base import Defense
from echo import functions


class ArmorAbsorb(Defense):
    name = "Armor Absorb"
    description = "Your Armor absorbs the damage."
    attacker_message = "but your attack glances off {defender_his} {defender_armor}!"
    observer_message = "but {attacker_his} glances off {defender_his} {defender_armor}!"

    @classmethod
    def evaluate(cls, attack_result):
        defender = attack_result.target_object
        effective_dex_modifier = defender.get_effective_dex_modifier()
        shield_modifier = defender.get_shield_modifiers()
        minimum_ac = 10 + effective_dex_modifier + shield_modifier
        maximum_ac = minimum_ac + defender.get_armor_modifiers()

        if minimum_ac <= attack_result.total_hit_roll <= maximum_ac:
            return True
        return False

    @classmethod
    def execute(cls, attack_result):
        return DefenseResult(message=cls.get_message(attack_result))

    @classmethod
    def get_message(cls, attack_result):
        defender = attack_result.target_object
        body_part_hit = attack_result.body_part_hit
        defender_armor = defender.equipment.worn_equipment_map.get(body_part_hit.instance)
        if defender_armor:
            defender_armor = defender_armor[0]

        if attack_result.attacker.is_player:
            return cls.attacker_message.format(
                defender_his=functions.his_her_it(attack_result.target_object),
                defender_armor=defender_armor.name if defender_armor else "armor"
            )
        else:
            return cls.observer_message.format(
                attacker_his=functions.his_her_it(attack_result.attacker),
                defender_his=functions.his_her_it(defender),
                defender_armor=defender_armor.name if defender_armor else "armor"
            )
