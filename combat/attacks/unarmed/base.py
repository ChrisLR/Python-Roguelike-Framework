from abilities.physical_abilities import PhysicalAbilities
from combat import targets
from combat.attackresult import AttackResult
from combat.attacks.base import Attack
from combat.enums import DamageType
from echo import functions
from stats.enums import StatsEnum
from util import check_roller, gridhelpers
from util.dice import Dice, DiceStack


class Punch(Attack):
    name = "Punch"
    target_type = targets.Single
    description = "Basic unarmed attack."

    actor_message = "You swing your fist at {defender}"
    observer_message = "{attacker} swings {attacker_his} fist at {defender}"

    @classmethod
    def can_execute(cls, attack_context):
        attacker = attack_context.attacker
        if attack_context.distance_to <= 1:
            attacker_body = attacker.body
            if attacker_body:
                return any([ability for ability in attacker_body.get_physical_abilities().keys()
                            if ability == PhysicalAbilities.PUNCH])
        return False

    @classmethod
    def execute(cls, attack_context):
        attacker = attack_context.attacker
        defender = attack_context.defender
        hit_modifier = attacker.get_stat_modifier(StatsEnum.Strength)
        attack_result = cls.make_hit_roll(attack_context, hit_modifier)
        attack_result.attack_message = cls.get_message(attacker, defender)
        attack_result.context.attacker_weapon = "fist"

        cls.make_damage_roll(attack_result, hit_modifier)

        return attack_result,

    @classmethod
    def make_damage_roll(cls, attack_result, str_modifier):
        melee_damage_dice = cls.get_melee_damage_dice(attack_result.context.attacker)
        total_damage = check_roller.roll_damage(
            dice_stacks=(melee_damage_dice,),
            modifiers=str_modifier,
            critical=attack_result.critical
        )
        attack_result.total_damage = total_damage
        attack_result.separated_damage = [(total_damage, DamageType.Blunt)]

        return attack_result

    @classmethod
    def get_melee_damage_dice(cls, actor):
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
