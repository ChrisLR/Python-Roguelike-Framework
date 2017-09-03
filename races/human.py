import bodies
from powers import racial
from races.base import Race
from stats.enums import Size
from util import languages
from util.abilityscoreset import AbilityScoreSet
from util.ageset import AgeSet
from util.alignmentset import AlignmentSet


class Human(Race):
    uid = "human"
    name = "Human"

    ability_score_adjustments = AbilityScoreSet.set_all(1)
    age_set = AgeSet(adult_age=18, elder_age=70, maximum_age=100)
    alignment_set = AlignmentSet()
    speed = 30
    size = Size.Medium
    average_height = 5
    average_weight = 180
    known_languages = (languages.Common, )
    racial_proficiencies = None
    body = bodies.HumanBody
    racial_powers = []
    racial_level_tree = None

    _possible_dragon_types = racial.DraconicAncestry.possible_types
    _breath_damage_types = racial.BreathWeapon.possible_damage_types
    _breath_target_types = racial.BreathWeapon.possible_target_types
    _possible_damage_resistance = racial.DamageResistance.possible_damage_types
    choices = {"bonus_language": [language for language in languages.listing if language not in known_languages]}

    def __init__(self, bonus_language):
        self.known_languages += bonus_language,
