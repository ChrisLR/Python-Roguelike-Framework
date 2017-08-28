from bodyparts import base
from combat.enums import ThreatLevel
from abilities.physical_abilities import PhysicalAbilities


class TrollishHand(base.Hand):
    uid = "trollish_hand"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {PhysicalAbilities.GRASP: 1, PhysicalAbilities.PUNCH: 1, PhysicalAbilities.CLAW: 1}


class TrollishFangs(base.Teeth):
    uid = "trollish_fangs"
    relative_size = 15
    threat_level = ThreatLevel.Major
    physical_abilities = {PhysicalAbilities.EAT: 1, PhysicalAbilities.BITE: 1}


class DraconianTeeth(base.Teeth):
    uid = "draconian_teeth"
    relative_size = 7
    threat_level = ThreatLevel.Major
    physical_abilities = {PhysicalAbilities.BITE: 1}


class DraconianTail(base.Tail):
    uid = "draconian_tail"
    relative_size = 25
    threat_level = ThreatLevel.Minor
    physical_abilities = None
