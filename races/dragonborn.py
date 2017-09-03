import bodies
from powers import racial
from races.base import Race
from stats.enums import Size, StatsEnum
from util import languages
from util.abilityscoreset import AbilityScoreSet
from util.ageset import AgeSet
from util.alignmentset import AlignmentSet


class Dragonborn(Race):
    uid = "dragonborn"
    name = "Dragonborn"

    ability_score_adjustments = AbilityScoreSet(strength=2, charisma=1)
    age_set = AgeSet(adult_age=15, elder_age=60, maximum_age=80)
    alignment_set = AlignmentSet(good=True, evil=True)
    speed = 30
    size = Size.Medium
    average_height = 6
    average_weight = 250
    known_languages = (languages.Common, languages.Draconic)
    racial_proficiencies = None
    body = bodies.DraconianBody
    racial_powers = []
    racial_level_tree = None

    _possible_dragon_types = racial.DraconicAncestry.possible_types
    _breath_damage_types = racial.BreathWeapon.possible_damage_types
    _breath_target_types = racial.BreathWeapon.possible_target_types
    _possible_damage_resistance = racial.DamageResistance.possible_damage_types
    choices = {"dragon_type": _possible_dragon_types}

    _breath_dragon_power_mapping = {
        _possible_dragon_types.Black: racial.BreathWeapon(
            breath_range=30, damage_type=_breath_damage_types.Acid,
            target_type=_breath_target_types.Line, save_stat=StatsEnum.Dexterity
        ),
        _possible_dragon_types.Blue: racial.BreathWeapon(
            breath_range=30, damage_type=_breath_damage_types.Lightning,
            target_type=_breath_target_types.Line, save_stat=StatsEnum.Dexterity
        ),
        _possible_dragon_types.Brass: racial.BreathWeapon(
            breath_range=30, damage_type=_breath_damage_types.Fire,
            target_type=_breath_target_types.Line, save_stat=StatsEnum.Dexterity
        ),
        _possible_dragon_types.Bronze: racial.BreathWeapon(
            breath_range=30, damage_type=_breath_damage_types.Lightning,
            target_type=_breath_target_types.Line, save_stat=StatsEnum.Dexterity
        ),
        _possible_dragon_types.Copper: racial.BreathWeapon(
            breath_range=30, damage_type=_breath_damage_types.Copper,
            target_type=_breath_target_types.Line, save_stat=StatsEnum.Dexterity
        ),
        _possible_dragon_types.Gold: racial.BreathWeapon(
            breath_range=15, damage_type=_breath_damage_types.Fire,
            target_type=_breath_target_types.Cone, save_stat=StatsEnum.Dexterity
        ),
        _possible_dragon_types.Green: racial.BreathWeapon(
            breath_range=15, damage_type=_breath_damage_types.Poison,
            target_type=_breath_target_types.Cone, save_stat=StatsEnum.Constitution
        ),
        _possible_dragon_types.Red: racial.BreathWeapon(
            breath_range=15, damage_type=_breath_damage_types.Fire,
            target_type=_breath_target_types.Cone, save_stat=StatsEnum.Dexterity
        ),
        _possible_dragon_types.Silver: racial.BreathWeapon(
            breath_range=15, damage_type=_breath_damage_types.Cold,
            target_type=_breath_target_types.Cone, save_stat=StatsEnum.Constitution
        ),
        _possible_dragon_types.White: racial.BreathWeapon(
            breath_range=15, damage_type=_breath_damage_types.Cold,
            target_type=_breath_target_types.Cone, save_stat=StatsEnum.Constitution
        ),
    }

    _damage_resistance_dragon_power_mapping = {
        _possible_dragon_types.Black: _possible_damage_resistance.Acid,
        _possible_dragon_types.Blue: _possible_damage_resistance.Lightning,
        _possible_dragon_types.Brass: _possible_damage_resistance.Fire,
        _possible_dragon_types.Bronze: _possible_damage_resistance.Lightning,
        _possible_dragon_types.Copper: _possible_damage_resistance.Acid,
        _possible_dragon_types.Gold: _possible_damage_resistance.Fire,
        _possible_dragon_types.Green: _possible_damage_resistance.Poison,
        _possible_dragon_types.Red: _possible_damage_resistance.Fire,
        _possible_dragon_types.Silver: _possible_damage_resistance.Cold,
        _possible_dragon_types.White: _possible_damage_resistance.Cold,
    }

    def __init__(self, dragon_type):
        self.racial_powers.append(racial.DraconicAncestry(dragon_type))
        self.racial_powers.append(self._breath_dragon_power_mapping[dragon_type])
        self.racial_powers.append(self._damage_resistance_dragon_power_mapping[dragon_type])
