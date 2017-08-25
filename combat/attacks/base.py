import abc
from util import check_roller
from combat import AttackResult


class Attack(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def name(cls):
        pass

    @abc.abstractclassmethod
    def description(cls):
        pass

    @abc.abstractclassmethod
    def target_type(cls):
        pass

    @abc.abstractclassmethod
    def can_execute(cls, attack_context):
        pass

    @abc.abstractclassmethod
    def execute(cls, attack_context):
        pass

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
