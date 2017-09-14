import random

import bodies
import races
from characters.character import Character
from components.display import Display
from components.outfitter import Outfitter
from components.stats import CharacterStats
from data.python_templates import classes as character_classes
from util.colors import Colors
from util.abilityscoreset import AbilityScoreSet

weak_orc = Character(
    uid="weak_orc",
    name="Weak Orc",
    character_class=character_classes.warrior_class,
    character_race=races.Orc(),
    stats=CharacterStats(AbilityScoreSet.set_all(8)),
    display=Display(Colors.DARK_OLIVE_GREEN, Colors.BLACK, "O"),
    body=bodies.OrcishBody(),
)
strong_orc = Character(
    uid="strong_orc",
    name="Strong Orc",
    character_class=character_classes.warrior_class,
    character_race=races.Orc(),
    stats=CharacterStats(AbilityScoreSet.set_all(8, strength=12, constitution=12)),
    display=Display(Colors.DARK_OLIVE_GREEN, Colors.BLACK, "O"),
    body=bodies.OrcishBody(),
)
weak_troll = Character(
    uid="weak_troll",
    name="Weak Troll",
    character_class=character_classes.warrior_class,
    character_race=races.Troll(),
    stats=CharacterStats(AbilityScoreSet.set_all(8, strength=14, constitution=14)),
    display=Display(Colors.DARK_GREEN, Colors.BLACK, "O"),
    body=bodies.TrollishBody(),
)
human_warrior = Character(
    uid="human_warrior",
    name="Human Warrior",
    character_class=character_classes.warrior_class,
    character_race=races.Human(),
    stats=CharacterStats(AbilityScoreSet.set_all(8, strength=12, constitution=12, dexterity=10)),
    display=Display(Colors.WHITE, Colors.BLACK, "O"),
    body=bodies.HumanBody(),
)
human_warrior.register_component(Outfitter('starter_warrior'))
human_thief = Character(
    uid="human_thief",
    name="Human Thief",
    character_class=character_classes.thief_class,
    character_race=races.Human(),
    stats=CharacterStats(AbilityScoreSet.set_all(8, constitution=10, dexterity=16)),
    display=Display(Colors.WHITE, Colors.BLACK, "O"),
    body=bodies.HumanBody(),
)
human_thief.register_component(Outfitter('starter_thief'))


# TODO Dog and Wolf are disabled until Monsters are refactored.
# dog = Character(
#     uid="dog",
#     name="Dog",
#     character_class=character_classes.canid_class,
#     character_race=races.dog_race,
#     stats=make_character_stats(health=5, constitution=12, dexterity=14, strength=13,
#                                intelligence=3, wisdom=12, charisma=7),
#     display=Display(Colors.WHITE, Colors.BLACK, "d"),
#     body=bodies.DogBody(),
# )
#
# wolf = Character(
#     uid="wolf",
#     name="Wolf",
#     character_class=character_classes.canid_class,
#     character_race=races.wolf_race,
#     stats=make_character_stats(health=11, constitution=12, dexterity=15, strength=12,
#                                intelligence=3, wisdom=12, charisma=6),
#     display=Display(Colors.WHITE, Colors.BLACK, "w"),
#     body=bodies.WolfBody(),
# )


character_templates = {
    weak_orc.uid: weak_orc,
    strong_orc.uid: strong_orc,
    weak_troll.uid: weak_troll,
    human_warrior.uid: human_warrior,
    human_thief.uid: human_thief,
}
