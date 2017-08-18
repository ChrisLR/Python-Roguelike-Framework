from combat import targets
from combat.attackresult import AttackResult
from combat.attacks.base import Attack
from combat.enums import DamageType
from echo import functions
from stats.enums import StatsEnum
from util import check_roller
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
    def can_execute(cls, actor, target):
        return any(actor.equipment.get_wielded_items())

    @classmethod
    def execute(cls, actor, target):
        attack_results = []
        weapons = cls.get_used_weapons(actor)
        dual_wield_modifier = 0
        if any((weapon for weapon in weapons if not weapon.weapon or not weapon.weapon.light)):
            dual_wield_modifier = -2

        target_ac = target.get_armor_class()
        is_offhand = False
        for weapon in weapons:
            stat_used, hit_modifier = cls.get_stat_used(actor, weapon)
            hit_modifier -= dual_wield_modifier
            attack_result = cls.make_hit_roll(actor, target, hit_modifier, target_ac)
            attack_result.attack_message = cls.get_message_for_weapon(actor, weapon, target)
            attack_result.attacker_weapon = weapon
            str_modifier = hit_modifier if stat_used == StatsEnum.Strength \
                else actor.get_stat_modifier(StatsEnum.Strength)

            cls.make_damage_roll(actor, attack_result, weapon, str_modifier, is_offhand)

            attack_results.append(attack_result)
            is_offhand = True

        return attack_results

    @classmethod
    def get_used_weapons(cls, attacker):
        """
        This Method will return the real wielded weapons.
        If none it will return anything that is wielded (Improvised Weapon)
        :param attacker: GameObject that is attacking
        :return: List of Items or None
        """
        items = attacker.equipment.get_wielded_items()
        weapons = [item for item in items if item.weapon]

        if weapons:
            return weapons
        else:
            return items

    @classmethod
    def get_stat_used(cls, attacker, weapon_item):
        weapon_component = weapon_item.weapon
        str_modifier = attacker.get_stat_modifier(StatsEnum.Strength)
        if weapon_component and weapon_component.finesse:
            dex_modifier = attacker.get_stat_modifier(StatsEnum.Dexterity)
            if dex_modifier > str_modifier:
                return StatsEnum.Dexterity, dex_modifier

        return StatsEnum.Strength, str_modifier

    @classmethod
    def make_hit_roll(cls, attacker, defender, hit_modifier, target_ac):
        success, critical, natural_roll, total_hit_roll = check_roller.d20_check_roll(
            difficulty_class=target_ac,
            modifiers=hit_modifier
        )
        return AttackResult(
            success=success,
            critical=critical,
            attacker=attacker,
            target_object=defender,
            target_ac=target_ac,
            natural_roll=natural_roll,
            total_hit_roll=total_hit_roll,
        )

    @classmethod
    def make_damage_roll(cls, attacker, attack_result, weapon_item, str_modifier, is_offhand=False):
        damage_dice = cls.get_damage_dice(weapon_item)
        total_damage = check_roller.roll_damage(
            dice_stacks=(damage_dice, ),
            modifiers=cls.get_damage_bonus(attacker, weapon_item, str_modifier, is_offhand),
            critical=attack_result.critical
        )
        attack_result.total_damage = total_damage
        attack_result.separated_damage = [(total_damage, cls.get_melee_damage_type(weapon_item))]

        return attack_result

    @classmethod
    def get_damage_bonus(cls, attacker, weapon_item, str_modifier=None, is_offhand=False):
        # TODO Weapon could have a damage bonus here.
        # TODO Some weapons held in one hand could also give a bonus here.
        if is_offhand:
            return 0

        if str_modifier is None:
            str_modifier = attacker.get_stat_modifier(StatsEnum.Strength)

        return str_modifier

    @classmethod
    def get_damage_dice(cls, weapon_item):
        weapon = weapon_item.weapon
        if weapon:
            return weapon_item.weapon.damage_dice
        return DiceStack(1, Dice(4))

    @classmethod
    def get_melee_damage_type(cls, item):
        if item.weapon:
            return item.weapon.melee_damage_type
        else:
            return DamageType.Blunt

    @classmethod
    def get_message_for_weapon(cls, actor, weapon_item, target):
        damage_type = cls.get_melee_damage_type(weapon_item)
        if actor.is_player:
            return cls.actor_attack_messages_per_damage_type[damage_type].format(
                attacker_weapon=weapon_item.name,
                defender=target.name
            )
        else:
            return cls.observer_attack_messages_per_damage_type[damage_type].format(
                attacker=actor.name,
                attacker_his=functions.his_her_it(actor),
                attacker_weapon=weapon_item.name,
                defender=target.name if not target.is_player else "you"
            )

