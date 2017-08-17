class AttackResult(object):
    """
    A class to keep a combat attack result organized across functions.
    """
    __slots__ = ['success', 'critical', 'target_object', 'attacker_weapon',
                 'natural_roll', 'total_hit_roll', 'total_damage', "attack_message",
                 'separated_damage', 'target_ac', 'body_part_hit', 'attacker']

    def __init__(self, success, critical, attacker, target_object, target_ac,
                 message, natural_roll=None, total_hit_roll=None, total_damage=None,
                 separated_damage=None, attacker_weapon=None):

        self.success = success
        self.critical = critical
        self.attacker_weapon = attacker_weapon
        self.natural_roll = natural_roll
        self.total_hit_roll = total_hit_roll
        self.total_damage = total_damage
        self.separated_damage = separated_damage
        self.target_object = target_object
        self.target_ac = target_ac
        self.body_part_hit = None
        self.attacker = attacker
        self.attack_message = attack_message

    def __str__(self):
        return "Rolled {} vs AC:{}".format(self.total_hit_roll, self.target_ac)