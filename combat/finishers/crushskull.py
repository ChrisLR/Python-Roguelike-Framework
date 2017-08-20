from combat.finishers.base import Finisher
from combat import attacks
from combat.enums import DamageType
from echo import functions


class CrushSkull(Finisher):
    name = "Crush Skull"
    description = "Crush the skull of your enemy."
    attacker_message = "You swing your {attacker_weapon} into a powerful overhead swing" \
                       " CRUSHING {defender_his} head like an overripe melon!"

    observer_message = "{attacker} swings {attacker_his} {attacker_weapon} into a powerful " \
                       "overhead swing CRUSHING {defender_his} head like an overripe melon!" \


    @classmethod
    def evaluate(cls, attack_result):
        attacker_weapon = attack_result.attacker_weapon
        if attacker_weapon and hasattr(attacker_weapon, 'weapon'):
            weapon_component = attacker_weapon.weapon
            if weapon_component:
                if weapon_component.melee_damage_type == DamageType.Blunt:
                    return True
        return False

    @classmethod
    def execute(cls, attack_result):
        return cls.get_message(attack_result)

    @classmethod
    def get_message(cls, attack_result):
        defender = attack_result.target_object
        if attack_result.attacker.is_player:
            return cls.attacker_message.format(
                attacker_weapon=functions.get_name_or_string(attack_result.attacker_weapon),
                defender_his=functions.his_her_it(defender),
            )
        else:
            return cls.observer_message.format(
                attacker=functions.get_name_or_string(attack_result.attacker),
                attacker_his=functions.his_her_it(attack_result.attacker),
                attacker_weapon=functions.get_name_or_string(attack_result.attacker_weapon),
                defender_his=functions.his_her_it(defender),
            )
