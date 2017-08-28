import bodies
import proficiencies
from powers import racial
from races.base import Race
from stats.enums import Size
from util import languages
from util.abilityscoreset import AbilityScoreSet
from util.ageset import AgeSet
from util.alignmentset import AlignmentSet


class Orc(Race):
    uid = "orc"
    name = "Orc"

    ability_score_adjustments = AbilityScoreSet(strength=2, constitution=2, intelligence=-2)
    age_set = AgeSet(adult_age=13, elder_age=37, maximum_age=50)
    alignment_set = AlignmentSet(chaos=True, evil=True)
    speed = 30
    size = Size.Medium
    average_height = 6
    average_weight = 220
    known_languages = (languages.Common, languages.Orcish)
    racial_proficiencies = (
        proficiencies.GreatAxe,
        proficiencies.Hide,
        proficiencies.Intimidation,
        proficiencies.Javelin
    )
    body = bodies.OrcishBody
    racial_powers = (
        racial.Aggressive,
        racial.RelentlessEndurance,
        racial.Darkvision
    )
