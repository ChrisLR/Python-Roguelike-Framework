from bodyparts import base
from combat.enums import ThreatLevel
from abilities.physical_abilities import PhysicalAbilities


class HumanoidHead(base.Head):
    uid = "humanoid_head"
    name = "Humanoid Head"
    relative_size = 25
    threat_level = ThreatLevel.Major
    physical_abilities = None


class HumanoidNeck(base.Neck):
    uid = "humanoid_neck"
    name = "Humanoid Neck"
    relative_size = 10
    threat_level = ThreatLevel.Critical
    physical_abilities = None


class HumanoidTorso(base.Torso):
    uid = "humanoid_torso"
    name = "Humanoid Torso"
    relative_size = 50
    threat_level = ThreatLevel.Major
    physical_abilities = None


class HumanoidArm(base.Arm):
    uid = "humanoid_arm"
    name = "Humanoid Arm"
    relative_size = 25
    threat_level = ThreatLevel.Major
    physical_abilities = None


class HumanoidLeg(base.Leg):
    uid = "humanoid_leg"
    name = "Humanoid Leg"
    relative_size = 25
    threat_level = ThreatLevel.Major
    physical_abilities = {PhysicalAbilities.STAND: 1, PhysicalAbilities.MOVE: 1}


class HumanoidHand(base.Hand):
    uid = "humanoid_hand"
    name = "Humanoid Hand"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {PhysicalAbilities.GRASP: 1, PhysicalAbilities.PUNCH: 1}


class HumanoidFoot(base.Foot):
    uid = "humanoid_foot"
    name = "Humanoid Foot"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {PhysicalAbilities.STAND: 1, PhysicalAbilities.MOVE: 1}


class HumanoidEye(base.Eye):
    uid = "humanoid_eye"
    name = "Humanoid Eye"
    relative_size = 5
    threat_level = ThreatLevel.Critical
    physical_abilities = {PhysicalAbilities.SEE: 1}


class HumanoidEar(base.Ear):
    uid = "humanoid_ear"
    name = "Humanoid Ear"
    relative_size = 5
    threat_level = ThreatLevel.Minor
    physical_abilities = {PhysicalAbilities.SEE: 1}


class HumanoidMouth(base.Mouth):
    uid = "humanoid_mouth"
    name = "Humanoid Mouth"
    relative_size = 5
    threat_level = ThreatLevel.Minor
    physical_abilities = {PhysicalAbilities.EAT: 1}


class HumanoidBrain(base.Brain):
    uid = "humanoid_brain"
    name = "Humanoid Brain"
    relative_size = 15
    threat_level = ThreatLevel.Fatal
    physical_abilities = {PhysicalAbilities.THINK: 1}


class HumanoidHeart(base.Heart):
    uid = "humanoid_heart"
    name = "Humanoid Heart"
    relative_size = 25
    threat_level = ThreatLevel.Fatal
    physical_abilities = {PhysicalAbilities.LIVE: 1}


class HumanoidLungs(base.Lungs):
    uid = "humanoid_lungs"
    name = "Humanoid Lungs"
    relative_size = 25
    threat_level = ThreatLevel.Fatal
    physical_abilities = {PhysicalAbilities.BREATHE: 1}
