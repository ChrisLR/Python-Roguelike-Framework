import abilities
from bodyparts import base
from combat.enums import ThreatLevel
from util import dice


class DraconianHand(base.Hand):
    uid = "draconian_hand"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Grasp(1), abilities.Punch(1), abilities.Claw(1, dice.D4)}


class DraconianFoot(base.Foot):
    uid = "draconian_foot"
    relative_size = 10
    threat_level = ThreatLevel.Minor
    physical_abilities = {abilities.Stand(1), abilities.Claw(1, dice.D4)}


class DraconianMuzzle(base.Muzzle):
    uid = "draconian_muzzle"
    relative_size = 15
    threat_level = ThreatLevel.Major
    physical_abilities = {abilities.Eat(1)}


class DraconianTeeth(base.Teeth):
    uid = "draconian_teeth"
    relative_size = 7
    threat_level = ThreatLevel.Major
    physical_abilities = {abilities.Bite(1)}


class DraconianTail(base.Tail):
    uid = "draconian_tail"
    relative_size = 25
    threat_level = ThreatLevel.Minor
    physical_abilities = None
