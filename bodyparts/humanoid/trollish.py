from bodyparts import base
from combat.enums import ThreatLevel
import abilities


class TrollishHand(base.Hand):
    uid = "trollish_hand"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Grasp(1), abilities.Punch(1), abilities.Claw()}


class TrollishFangs(base.Teeth):
    uid = "trollish_fangs"
    relative_size = 15
    threat_level = ThreatLevel.Major
    physical_abilities = {PhysicalAbilities.EAT: 1, PhysicalAbilities.BITE: 1}
