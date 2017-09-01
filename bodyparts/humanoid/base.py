import abilities
from bodyparts import base
from combat.enums import ThreatLevel


class HumanoidHead(base.Head):
    uid = "humanoid_head"
    relative_size = 25
    threat_level = ThreatLevel.Major
    physical_abilities = None


class HumanoidNeck(base.Neck):
    uid = "humanoid_neck"
    relative_size = 10
    threat_level = ThreatLevel.Critical
    physical_abilities = None


class HumanoidTorso(base.Torso):
    uid = "humanoid_torso"
    relative_size = 50
    threat_level = ThreatLevel.Major
    physical_abilities = None


class HumanoidArm(base.Arm):
    uid = "humanoid_arm"
    relative_size = 25
    threat_level = ThreatLevel.Major
    physical_abilities = None


class HumanoidLeg(base.Leg):
    uid = "humanoid_leg"
    relative_size = 25
    threat_level = ThreatLevel.Major
    physical_abilities = {abilities.Stand(1)}


class HumanoidHand(base.Hand):
    uid = "humanoid_hand"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Grasp(1), abilities.Punch(1)}


class HumanoidFoot(base.Foot):
    uid = "humanoid_foot"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Stand(1)}


class HumanoidEye(base.Eye):
    uid = "humanoid_eye"
    relative_size = 5
    threat_level = ThreatLevel.Critical
    physical_abilities = {abilities.See(1)}


class HumanoidEar(base.Ear):
    uid = "humanoid_ear"
    relative_size = 5
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Hear(1)}


class HumanoidMouth(base.Mouth):
    uid = "humanoid_mouth"
    relative_size = 5
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Eat(1), abilities.Breathe(1)}


class HumanoidNose(base.Mouth):
    uid = "humanoid_nose"
    relative_size = 5
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Smell(1), abilities.Breathe(1)}


class HumanoidBrain(base.Brain):
    uid = "humanoid_brain"
    relative_size = 15
    threat_level = ThreatLevel.Fatal
    physical_abilities = {abilities.Think(1)}


class HumanoidHeart(base.Heart):
    uid = "humanoid_heart"
    relative_size = 25
    threat_level = ThreatLevel.Fatal
    physical_abilities = {}


class HumanoidLungs(base.Lungs):
    uid = "humanoid_lungs"
    relative_size = 25
    threat_level = ThreatLevel.Fatal
    physical_abilities = {abilities.Breathe}


class HumanoidTeeth(base.Teeth):
    uid = "humanoid_teeth"
    relative_size = 5
    threat_level = ThreatLevel.Major
    physical_abilities = {abilities.Bite(0.5)}
