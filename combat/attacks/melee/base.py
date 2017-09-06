from combat import targets
from combat.attackresult import AttackResult
from combat.attacks.base import Attack
from combat.enums import DamageType
from echo import functions
from stats.enums import StatsEnum
from util import check_roller, gridhelpers
from util.dice import Dice, DiceStack


class MeleeAttack(Attack):
    name = "Melee Attack"
    target_type = targets.Single
    description = "Basic attack for any weapons."

    actor_attack_messages_per_damage_type = {
        DamageType.Blunt: "You smash your {attacker_weapon} at {defender}",
        DamageType.Pierce: "You stab your {attacker_weapon} at {defender}",
        DamageType.Slash: "You slash your {attacker_weapon} at {defender}",
    }
    observer_attack_messages_per_damage_type = {
        DamageType.Blunt: "{attacker} smashes {attacker_his} {attacker_weapon} at {defender}",
        DamageType.Pierce: "{attacker} stabs {attacker_his} {attacker_weapon} at {defender}",
        DamageType.Slash: "{attacker} slashes {attacker_his} {attacker_weapon} at {defender}",
    }

    @classmethod
    def can_execute(cls, attack_context):
        attacker = attack_context.attacker
        return any(attacker.equipment.get_wielded_items()) and attack_context.distance_to <= 1

    @classmethod
    def execute(cls, attack_context):
        attack_results = []
        weapons = cls.get_used_weapons(attack_context)
        dual_wield_modifier = 0
        if any((weapon for weapon in weapons if not weapon.weapon or not weapon.weapon.light)):
            dual_wield_modifier = -2

        is_offhand = False
        for weapon in weapons:
            attack_context.attacker_weapon = weapon
            stat_used, hit_modifier = cls.get_stat_used(attack_context)
            hit_modifier -= dual_wield_modifier
            attack_result = cls.make_hit_roll(attack_context, hit_modifier)
            attack_result.attack_message = cls.get_message_for_weapon(attack_context)
            attack_result.context.attacker_weapon = weapon
            str_modifier = hit_modifier if stat_used == StatsEnum.Strength \
                else attack_context.attacker.stats.strength.modifier

            cls.make_damage_roll(attack_result, weapon, str_modifier, is_offhand)

            attack_results.append(attack_result)
            is_offhand = True

        return attack_results

    @classmethod
    def get_used_weapons(cls, attack_context):
        """
        This Method will return the real wielded weapons.
        If none it will return anything that is wielded (Improvised Weapon)
        :param attack_context: AttackContext instance
        :return: List of Items or None
        """
        items = attack_context.attacker.equipment.get_wielded_items()
        weapons = [item for item in items if item.weapon]

        if weapons:
            return weapons
        else:
            return items

    @classmethod
    def get_stat_used(cls, attack_context):
        attacker = attack_context.attacker
        weapon_component = attack_context.attacker_weapon.weapon
        str_modifier = attacker.stats.strength.modifier
        if weapon_component and weapon_component.finesse:
            dex_modifier = attacker.stats.dexterity.modifier
            if dex_modifier > str_modifier:
                return StatsEnum.Dexterity, dex_modifier

        return StatsEnum.Strength, str_modifier

    @classmethod
    def make_damage_roll(cls, attack_result, weapon_item, str_modifier, is_offhand=False):
        melee_damage_dice = cls.get_melee_damage_dice(weapon_item)
        total_damage = check_roller.roll_damage(
            dice_stacks=(melee_damage_dice, ),
            modifiers=cls.get_damage_bonus(attack_result, str_modifier, is_offhand),
            critical=attack_result.critical
        )
        attack_result.total_damage = total_damage
        attack_result.separated_damage = [(total_damage, cls.get_melee_damage_type(weapon_item))]

        return attack_result

    @classmethod
    def get_damage_bonus(cls, attack_result, str_modifier=None, is_offhand=False):
        # TODO Weapon could have a damage bonus here.
        # TODO Some weapons held in one hand could also give a bonus here.
        if is_offhand:
            return 0

        if str_modifier is None:
            str_modifier = attack_result.attacker.stats.strength.modifier

        return str_modifier

    @classmethod
    def get_melee_damage_dice(cls, weapon_item):
        weapon = weapon_item.weapon
        if weapon:
            return weapon_item.weapon.melee_damage_dice
        return DiceStack(1, dice.D4)

    @classmethod
    def get_melee_damage_type(cls, item):
        if item.weapon:
            return item.weapon.melee_damage_type
        else:
            return DamageType.Blunt

    @classmethod
    def get_message_for_weapon(cls, attack_context):
        attacker_weapon = attack_context.attacker_weapon
        attacker = attack_context.attacker
        defender = attack_context.defender

        damage_type = cls.get_melee_damage_type(attacker_weapon)
        if attacker.is_player:
            return cls.actor_attack_messages_per_damage_type[damage_type].format(
                attacker_weapon=attacker_weapon.name,
                defender=defender.name
            )
        else:
            return cls.observer_attack_messages_per_damage_type[damage_type].format(
                attacker=attacker.name,
                attacker_his=functions.his_her_it(attacker),
                attacker_weapon=attacker_weapon.name,
                defender=functions.name_or_you(defender)
            )
