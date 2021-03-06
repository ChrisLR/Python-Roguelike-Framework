from combat.enums import DamageType
from combat.finishers.base import Finisher
from echo import functions
from util import gridhelpers


class Impale(Finisher):
    name = "Impale"
    description = "Impale your enemy with a slashing or piercing weapon."
    attacker_message = "You impale {defender}'s {defender_bodypart} with your {attacker_weapon}"
    observer_message = "{attacker} impales {defender} {defender_bodypart} with {attacker_his} {attacker_weapon}"

    @classmethod
    def evaluate(cls, attack_result):
        if attack_result.context.distance_to <= 1:
            attacker_weapon = attack_result.context.attacker_weapon
            if attacker_weapon and hasattr(attacker_weapon, 'weapon'):
                weapon_component = attacker_weapon.weapon
                if weapon_component:
                    if weapon_component.melee_damage_type in (DamageType.Pierce, DamageType.Slash):
                        return True
        return False

    @classmethod
    def execute(cls, attack_result):
        return cls.get_message(attack_result)

    @classmethod
    def get_message(cls, attack_result):
        attacker = attack_result.context.attacker
        defender = attack_result.context.defender
        attacker_weapon = attack_result.context.attacker_weapon
        if attacker.is_player:
            message = cls.attacker_message.format(
                defender=defender.name,
                defender_bodypart=attack_result.body_part_hit.name,
                attacker_weapon=attacker_weapon.name,
            )
        else:
            message = cls.observer_message.format(
                attacker=functions.get_name_or_string(attacker),
                defender=functions.names_or_your(defender),
                defender_bodypart=attack_result.body_part_hit.name,
                attacker_his=functions.his_her_it(attacker),
                attacker_weapon=attacker_weapon.name
            )

        if defender.body.blood:
            message += " splashing {blood} behind {defender_him}!!\n".format(
                blood=defender.body.blood.name,
                defender_him=functions.him_her_it(defender)
            )

        return message
