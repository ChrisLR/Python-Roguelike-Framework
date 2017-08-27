import bodies
from races.base import Race
from stats.enums import Size
from util.abilityscoreset import AbilityScoreSet
from util.ageset import AgeSet
from util.alignmentset import AlignmentSet
from util import languages


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
    skill_proficiencies = None
    body = bodies.DraconianBody

