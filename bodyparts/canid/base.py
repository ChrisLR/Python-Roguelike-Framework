from bodyparts import base
from combat.enums import ThreatLevel
from abilities.physical_abilities import PhysicalAbilities


class CanidHead(base.Head):
    uid = "canid_head"
    relative_size = 25
    threat_level = ThreatLevel.Major
    physical_abilities = None


class CanidNeck(base.Neck):
    uid = "canid_neck"
    relative_size = 10
    threat_level = ThreatLevel.Critical
    physical_abilities = None


class CanidTorso(base.Torso):
    uid = "canid_torso"
    relative_size = 50
    threat_level = ThreatLevel.Major
    physical_abilities = None


class CanidForeleg(base.Leg):
    uid = "canid_foreleg"
    relative_size = 20
    threat_level = ThreatLevel.Major
    physical_abilities = {PhysicalAbilities.STAND: 1, PhysicalAbilities.MOVE: 1}


class CanidHindLeg(base.Leg):
    uid = "canid_hindleg"
    relative_size = 20
    threat_level = ThreatLevel.Major
    physical_abilities = {PhysicalAbilities.STAND: 1, PhysicalAbilities.MOVE: 1}


class CanidPaw(base.Hand):
    uid = "canid_paw"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {PhysicalAbilities.STAND: 1, PhysicalAbilities.MOVE: 1}


class CanidEye(base.Eye):
    uid = "canid_eye"
    relative_size = 5
    threat_level = ThreatLevel.Critical
    physical_abilities = {PhysicalAbilities.SEE: 1}


class CanidEar(base.Ear):
    uid = "humanoid_ear"
    relative_size = 5
    threat_level = ThreatLevel.Minor
    physical_abilities = {PhysicalAbilities.HEAR: 2}


class CanidMuzzle(base.Muzzle):
    uid = "canid_muzzle"
    relative_size = 15
    threat_level = ThreatLevel.Major
    physical_abilities = {PhysicalAbilities.EAT: 1}


class CanidNose(base.Mouth):
    uid = "canid_nose"
    relative_size = 5
    threat_level = ThreatLevel.Minor
    physical_abilities = {PhysicalAbilities.SMELL: 2, PhysicalAbilities.BREATHE: 1}


class CanidBrain(base.Brain):
    uid = "canid_brain"
    relative_size = 10
    threat_level = ThreatLevel.Fatal
    physical_abilities = {PhysicalAbilities.THINK: 1}


class CanidHeart(base.Heart):
    uid = "canid_heart"
    relative_size = 20
    threat_level = ThreatLevel.Fatal
    physical_abilities = {PhysicalAbilities.LIVE: 1}


class CanidLungs(base.Lungs):
    uid = "canid_lungs"
    relative_size = 20
    threat_level = ThreatLevel.Fatal
    physical_abilities = {PhysicalAbilities.BREATHE: 1}


class CanidFangs(base.Teeth):
    uid = "canid_fangs"
    relative_size = 5
    threat_level = ThreatLevel.Major
    physical_abilities = {PhysicalAbilities.BITE: 1}


class CanidTail(base.Tail):
    uid = "canid_tail"
    relative_size = 25
    threat_level = ThreatLevel.Minor
    physical_abilities = None
