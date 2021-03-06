from combat import targets
from combat.attackresult import AttackResult
from combat.attacks.ranged.base import RangedAttack
from combat.enums import DamageType
from echo import functions
from managers.echo import EchoService
from stats.enums import StatsEnum
from util import check_roller
from util.dice import DiceStack, Dice


class FireWeapon(RangedAttack):
    name = "Fire Weapon"
    description = "Basic fire a ranged weapon at an enemy."
    target_type = targets.Single

    actor_attack_message = "You fire an {ammo} at {defender}"
    observer_attack_message = "{attacker} fires an {ammo} at {defender}"

    @classmethod
    def can_execute(cls, attack_context):
        attacker_weapon = attack_context.attacker_weapon
        if attacker_weapon:
            weapon_component = attacker_weapon.weapon
            if weapon_component.ammunition_uid and attacker_weapon.weapon.ranged_damage_type:
                if weapon_component.long_range > attack_context.distance_to * 6:
                    return True
                else:
                    if attack_context.attacker.is_player:
                        EchoService.singleton.echo("You are too far away.")
        return False

    @classmethod
    def execute(cls, attack_context):
        attacker = attack_context.attacker
        defender = attack_context.defender

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
        hit_modifier = attacker.stats.dexterity.modifier

        attack_result = cls.make_hit_roll(attack_context, hit_modifier)
        attack_result.attack_message = cls.get_message(attacker, ammunition, defender)
        attack_result.context.attacker_weapon = ranged_weapon

        cls.make_damage_roll(attack_result, hit_modifier)

        return attack_result,

    @classmethod
    def make_hit_roll(cls, attack_context, hit_modifier):
        success, critical, natural_roll, total_hit_roll = check_roller.d20_check_roll(
            difficulty_class=attack_context.defender_ac,
            modifiers=hit_modifier
        )
        return AttackResult(
            success=success,
            critical=critical,
            context=attack_context,
            natural_roll=natural_roll,
            total_hit_roll=total_hit_roll,
        )

    @classmethod
    def make_damage_roll(cls, attack_result, modifier):
        attacker_weapon = attack_result.context.attacker_weapon
        melee_damage_dice = cls.get_ranged_damage_dice(attacker_weapon)
        total_damage = check_roller.roll_damage(
            dice_stacks=(melee_damage_dice,),
            modifiers=cls.get_damage_bonus(attack_result, modifier),
            critical=attack_result.critical
        )
        attack_result.total_damage = total_damage
        attack_result.separated_damage = [(total_damage, cls.get_ranged_damage_type(attacker_weapon))]

        return attack_result

    @classmethod
    def get_damage_bonus(cls, attack_result, modifier):
        # TODO Weapon could have a damage bonus here.
        # TODO Some weapons held in one hand could also give a bonus here.

        return modifier

    @classmethod
    def get_ranged_damage_dice(cls, weapon_item):
        weapon = weapon_item.weapon
        if weapon:
            return weapon_item.weapon.ranged_damage_dice
        return DiceStack(1, dice.D4)

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
