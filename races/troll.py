import bodies
import proficiencies
from powers import racial
from races.base import Race
from stats.enums import Size
from util import languages
from util.abilityscoreset import AbilityScoreSet
from util.ageset import AgeSet
from util.alignmentset import AlignmentSet


class Troll(Race):
    uid = "troll"
    name = "Troll"

    ability_score_adjustments = AbilityScoreSet(strength=2, constitution=2, charisma=-1)
    age_set = AgeSet(adult_age=10, elder_age=20, maximum_age=30)
    alignment_set = AlignmentSet(chaos=True, evil=True)
    speed = 30
    size = Size.Medium
    average_height = 7
    average_weight = 300
    known_languages = (languages.Giant, )
    racial_proficiencies = None
    body = bodies.TrollishBody
    racial_powers = [
        
    ]
