from combat import targets
from combat.attacks.ranged.base import RangedAttack
from combat.enums import DamageType
from echo import functions
from managers.echo import EchoService
from stats.enums import StatsEnum
from util import check_roller
from util.dice import DiceStack, Dice


class ThrowWeapon(RangedAttack):
    name = "Throw Weapon"
    description = "Basic throw a weapon at an enemy."
    target_type = targets.Single

    actor_attack_message = "You throw a {attacker_weapon} at {defender}"
    observer_attack_message = "{attacker} throws a {attacker_weapon} at {defender}"

    @classmethod
    def can_execute(cls, attack_context):
        attacker_weapon = attack_context.attacker_weapon
        if attacker_weapon:
            weapon_component = attacker_weapon.weapon
            if weapon_component.thrown:
                if weapon_component.long_range < attack_context.distance_to * 6:
                    return True
                else:
                    if attack_context.attacker.is_player:
                        EchoService.singleton.echo("You are too far away.")
        return False

    @classmethod
    def execute(cls, attack_context):
        attacker = attack_context.attacker
        defender = attack_context.defender
        attacker_weapon = attack_context.attacker_weapon
        hit_modifier = attacker.get_stat_modifier(StatsEnum.Dexterity)

        attack_result = cls.make_hit_roll(attack_context, hit_modifier)
        attack_result.attack_message = cls.get_message(attack_context)

        cls.make_damage_roll(attack_result, hit_modifier)
        attacker.equipment.remove_item(attacker_weapon)
        attacker_weapon.location = defender.location.copy()
        attacker.location.level.spawned_items.append(attacker_weapon)

        return attack_result,

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
        return DiceStack(1, Dice(4))

    @classmethod
    def get_ranged_damage_type(cls, item):
        if item.weapon:
            return item.weapon.ranged_damage_type
        else:
            return DamageType.Blunt

    @classmethod
    def get_message(cls, attack_context):
        attacker = attack_context.attacker
        defender = attack_context.defender
        attacker_weapon = attack_context.attacker_weapon
        if attacker.is_player:
            return cls.actor_attack_message.format(
                attacker_weapon=functions.get_name_or_string(attacker_weapon),
                defender=functions.name_or_you(defender)
            )
        else:
            return cls.observer_attack_message.format(
                attacker=attacker.name,
                attacker_weapon=functions.get_name_or_string(attacker_weapon),
                defender=functions.name_or_you(defender)
            )
