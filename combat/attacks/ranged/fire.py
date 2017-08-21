from combat.attacks.ranged.base import RangedAttack
from combat import targets
from combat.enums import DamageType
from combat.attackresult import AttackResult
from stats.enums import StatsEnum
from util import check_roller
from util.dice import DiceStack, Dice
from echo import functions
from managers.echo import EchoService


class FireWeapon(RangedAttack):
    name = "Fire Weapon"
    description = "Basic fire a ranged weapon at an enemy."
    target_type = targets.Single

    actor_attack_message = "You fire an {ammo} at {defender}"
    observer_attack_message = "{attacker} fires an {ammo} at {defender}"

    @classmethod
    def can_execute(cls, actor, target):
        ranged_weapon = next((item for item in actor.equipment.get_wielded_items()
                              if item.weapon and item.weapon.ranged_damage_type), None)

        if ranged_weapon:
            weapon_component = ranged_weapon.weapon
            if weapon_component.ammunition_uid:
                return True
        return False

    @classmethod
    def execute(cls, attacker, target):
        ranged_weapon = next((item for item in attacker.equipment.get_wielded_items()
                              if item.weapon and item.weapon.ranged_damage_type
                              and item.weapon.ammunition_uid), None)

        weapon_component = ranged_weapon.weapon
        ammunition = attacker.inventory.get_items(weapon_component.ammunition_uid, count=1, pop=True)
        if not ammunition:
            if attacker.is_player:
                EchoService.singleton.echo("You have no {} left to fire!".format(
                    weapon_component.ammunition_uid))
            return

        ammunition = ammunition[0]
        target_ac = target.get_armor_class()
        hit_modifier = attacker.get_stat_modifier(StatsEnum.Dexterity)

        attack_result = cls.make_hit_roll(attacker, target, hit_modifier, target_ac)
        attack_result.attack_message = cls.get_message(attacker, ammunition, target)
        attack_result.attacker_weapon = ranged_weapon

        cls.make_damage_roll(attacker, attack_result, ranged_weapon, hit_modifier)

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
