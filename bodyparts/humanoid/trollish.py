import abilities
from bodyparts import base
from combat.enums import ThreatLevel
from util import dice


class TrollishHand(base.Hand):
    uid = "trollish_hand"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Grasp(1), abilities.Punch(1), abilities.Claw(1, dice.D6)}


class TrollishFangs(base.Teeth):
    uid = "trollish_fangs"
    relative_size = 15
    threat_level = ThreatLevel.Major
    physical_abilities = {abilities.Bite(1)}
