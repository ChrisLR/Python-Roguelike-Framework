from abilities.ability import Ability
from abilities.power_abilities import PowerAbilities
from components.race import Race
from stats.enums import StatsEnum
from stats.stat import StatModifier
from util.leveltree import LevelTree


def build_orc_race():
    # An orc won't get uglier over time but it could gain abilities.
    orc_level_tree = LevelTree()
    orc_level_tree.stats_modifiers = {
        1: [
            StatModifier(StatsEnum.Strength, 2),
            StatModifier(StatsEnum.Constitution, 2),
            StatModifier(StatsEnum.Charisma, -2),
            StatModifier(StatsEnum.Intelligence, -2)
        ]
    }
    orc_level_tree.ability_modifiers = {
        1: [Ability(PowerAbilities.Berserk, 1)]
    }
    orc_race = Race("orc", "Orc", orc_level_tree, "orcish")

    return orc_race


def build_troll_race():
    troll_level_tree = LevelTree()
    troll_level_tree.stats_modifiers = {
        1: [
            StatModifier(StatsEnum.Strength, 4),
            StatModifier(StatsEnum.Constitution, 4),
            StatModifier(StatsEnum.Charisma, -4),
            StatModifier(StatsEnum.Intelligence, -4)
        ]
    }
    troll_level_tree.ability_modifiers = {
        1: [Ability(PowerAbilities.Regeneration, 1)]
    }
    troll_race = Race("troll", "Troll", troll_level_tree, "trollish")

    return troll_race


def build_human_race():
    human_level_tree = LevelTree()
    human_race = Race("human", "Human", human_level_tree, "human")

    return human_race


def build_dog_race():
    dog_level_tree = LevelTree()
    dog_race = Race("dog", "Dog", dog_level_tree, "dog")

    return dog_race


def build_wolf_race():
    wolf_level_tree = LevelTree()
    wolf_race = Race("wolf", "Wolf", wolf_level_tree, "wolf")

    return wolf_race

human_race = build_human_race()
orc_race = build_orc_race()
troll_race = build_troll_race()
dog_race = build_dog_race()
wolf_race = build_wolf_race()

race_templates = {
    human_race.uid: human_race,
    orc_race.uid: orc_race,
    troll_race.uid: troll_race,
    dog_race.uid: dog_race,
    wolf_race.uid: wolf_race,
}
