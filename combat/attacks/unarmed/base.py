from abilities.physical_abilities import PhysicalAbilities
from combat import targets
from combat.attackresult import AttackResult
from combat.attacks.base import Attack
from combat.enums import DamageType
from echo import functions
from stats.enums import StatsEnum
from util import check_roller
from util.dice import Dice, DiceStack


class Punch(Attack):
    name = "Punch"
    target_type = targets.Single
    description = "Basic unarmed attack."

    actor_message = "You swing your fist at {defender}"
    observer_message = "{attacker} swings {attacker_his} fist at {defender}"

    @classmethod
    def can_execute(cls, actor, target):
        actor_body = actor.body
        if actor_body:
            return any([ability for ability in actor_body.get_physical_abilities().keys()
                        if ability == PhysicalAbilities.PUNCH])
        return False

    @classmethod
    def execute(cls, actor, target):
        target_ac = target.get_armor_class()
        hit_modifier = actor.get_stat_modifier(StatsEnum.Strength)
        attack_result = cls.make_hit_roll(actor, target, hit_modifier, target_ac)
        attack_result.attack_message = cls.get_message(actor, target)

        cls.make_damage_roll(actor, attack_result, hit_modifier)

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
    def make_damage_roll(cls, attacker, attack_result, str_modifier):
        damage_dice = cls.get_damage_dice(attacker)
        total_damage = check_roller.roll_damage(
            dice_stacks=(damage_dice,),
            modifiers=str_modifier,
            critical=attack_result.critical
        )
        attack_result.total_damage = total_damage
        attack_result.separated_damage = [(total_damage, DamageType.Blunt)]

        return attack_result

    @classmethod
    def get_damage_dice(cls, actor):
        return DiceStack(1, Dice(actor.stats.get_current_value(StatsEnum.Size) - 1))

    @classmethod
    def get_message(cls, actor, target):
        if actor.is_player:
            return cls.actor_message.format(defender=target.name)
        else:
            return cls.observer_message.format(
                attacker=actor.name,
                attacker_his=functions.his_her_it(actor),
                defender=functions.name_or_you(target)
            )
