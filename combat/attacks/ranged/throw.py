from combat.attacks.ranged.base import RangedAttack
from combat import targets
from combat.enums import DamageType
from combat.attackresult import AttackResult
from stats.enums import StatsEnum
from util import check_roller
from util.dice import DiceStack, Dice
from echo import functions
from managers.echo import EchoService


class ThrowWeapon(RangedAttack):
    name = "Throw Weapon"
    description = "Basic throw a weapon at an enemy."
    target_type = targets.Single

    actor_attack_message = "You throw an {attacker_weapon} at {defender}"
    observer_attack_message = "{attacker} throws a {attacker_weapon} at {defender}"

    @classmethod
    def can_execute(cls, actor, target):
        return any((item for item in actor.equipment.get_wielded_items()))

    @classmethod
    def execute(cls, attacker, target):
        wielded_items = attacker.equipment.get_wielded_items()
        thrown_weapon = next((item for item in wielded_items if item.weapon and item.weapon.thrown), None)
        if not thrown_weapon:
            # Improvised throw, can throw anything
            thrown_weapon = wielded_items[0]
        else:
            weapon_component = thrown_weapon.weapon

        target_ac = target.get_armor_class()
        hit_modifier = attacker.get_stat_modifier(StatsEnum.Dexterity)

        attack_result = cls.make_hit_roll(attacker, target, hit_modifier, target_ac)
        attack_result.attack_message = cls.get_message(attacker, thrown_weapon, target)
        attack_result.context.attacker_weapon = thrown_weapon

        cls.make_damage_roll(attacker, attack_result, thrown_weapon, hit_modifier)

        return attack_result,

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
    def make_damage_roll(cls, attacker, attack_result, weapon_item, modifier):
        melee_damage_dice = cls.get_ranged_damage_dice(weapon_item)
        total_damage = check_roller.roll_damage(
            dice_stacks=(melee_damage_dice,),
            modifiers=cls.get_damage_bonus(attacker, weapon_item, modifier),
            critical=attack_result.critical
        )
        attack_result.total_damage = total_damage
        attack_result.separated_damage = [(total_damage, cls.get_ranged_damage_type(weapon_item))]

        return attack_result

    @classmethod
    def get_damage_bonus(cls, attacker, weapon_item, modifier):
        # TODO Weapon could have a damage bonus here.
        # TODO Some weapons held in one hand could also give a bonus here.

        return modifier

    @classmethod
    def get_ranged_damage_dice(cls, weapon_item):
        weapon = weapon_item.weapon
        if weapon:
            return weapon_item.weapon.ranged_damage_dice
        return DiceStack(1, Dice(4))

    @classmethod
    def get_ranged_damage_type(cls, item):
        if item.weapon:
            return item.weapon.ranged_damage_type
        else:
            return DamageType.Blunt

    @classmethod
    def get_message(cls, actor, ammo, target):
        if actor.is_player:
            return cls.actor_attack_message.format(
                ammo=functions.get_name_or_string(ammo),
                defender=functions.name_or_you(target)
            )
        else:
            return cls.observer_attack_message.format(
                attacker=actor.name,
                ammo=functions.get_name_or_string(ammo),
                defender=functions.name_or_you(target)
            )
