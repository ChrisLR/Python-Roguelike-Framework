class AttackResult(object):
    """
    A class to keep a combat attack result organized across functions.
    """
    __slots__ = ['success', 'critical', 'context',
                 'natural_roll', 'total_hit_roll', 'total_damage', "attack_message",
                 'separated_damage', 'body_part_hit', 'damage_message']

    def __init__(self, success, critical, context,
                 attack_message="", damage_message="",
                 natural_roll=None, total_hit_roll=None,
                 total_damage=None, separated_damage=None):

        self.success = success
        self.critical = critical
        self.context = context
        self.natural_roll = natural_roll
        self.total_hit_roll = total_hit_roll
        self.total_damage = total_damage
        self.separated_damage = separated_damage
        self.body_part_hit = None
        self.attack_message = attack_message
        self.damage_message = damage_message

    def __str__(self):
        return "Rolled {} vs AC:{}".format(self.total_hit_roll, self.context.defender_ac)
