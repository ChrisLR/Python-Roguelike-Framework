import abilities
from bodyparts import base
from combat.enums import ThreatLevel
from util import dice


class TrollishHand(base.Hand):
    uid = "trollish_hand"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Grasp(0.5), abilities.Punch(1), abilities.Claw(1, dice.D6)}


class LargeTrollishHand(base.Hand):
    uid = "large_trollish_hand"
    relative_size = 15
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Grasp(0.5), abilities.Punch(1), abilities.Claw(2, dice.D4)}


class VeryLargeTrollishHand(base.Hand):
    uid = "very_large_trollish_hand"
    relative_size = 20
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Grasp(0.5), abilities.Punch(1), abilities.Claw(2, dice.D6)}


class TrollishFangs(base.Teeth):
    uid = "trollish_fangs"
    relative_size = 15
    threat_level = ThreatLevel.Major
    physical_abilities = {abilities.Bite(1)}
