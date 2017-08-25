from util import gridhelpers


class AttackContext(object):
    __slots__ = ['attacker', 'defender', 'attacker_weapon', 'attack_used', 'defender_ac', 'distance_to', 'ranged']

    def __init__(self, attacker, defender, attacker_weapon=None, attack_used=None, ranged=False):
        self.attacker = attacker
        self.defender = defender
        self.attacker_weapon = attacker_weapon
        self.attack_used = attack_used
        self.defender_ac = defender.get_armor_class()
        self.distance_to = gridhelpers.distance_to(attacker, defender)
        self.ranged = ranged

    # TODO WE SHOULD PROVIDE THE DEFENDER_AC AND THE DISTANCE_TO AS THEY ARE REFERRED OFTEN.
