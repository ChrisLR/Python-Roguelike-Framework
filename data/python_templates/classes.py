from abilities.ability import Ability
from abilities.power_abilities import PowerAbilities
from components.character_class import CharacterClass
from util.leveltree import LevelTree


def build_warrior_class():
    warrior_level_tree = LevelTree()
    warrior_level_tree.add_ability_modifier(2, Ability(PowerAbilities.PowerAttack, 1, level_progression=2))
    warrior_level_tree.add_ability_modifier(4, Ability(PowerAbilities.Parry, 1, level_progression=4))

    return CharacterClass('warrior', 'Warrior', warrior_level_tree, hit_die=10)


def build_thief_class():
    thief_level_tree = LevelTree()
    thief_level_tree.add_ability_modifier(2, Ability(PowerAbilities.Sneak, 1, level_progression=2))
    thief_level_tree.add_ability_modifier(4, Ability(PowerAbilities.Backstab, 1, level_progression=4))

    return CharacterClass('thief', 'Thief', thief_level_tree, hit_die=8)


def build_ranger_class():
    ranger_level_tree = LevelTree()
    ranger_level_tree.add_ability_modifier(2, Ability(PowerAbilities.Parry, 1, level_progression=2))
    ranger_level_tree.add_ability_modifier(4, Ability(PowerAbilities.Sneak, 1, level_progression=4))

    return CharacterClass('ranger', 'Ranger', ranger_level_tree, hit_die=10)


def build_canid_class():
    canid_level_tree = LevelTree()

    return CharacterClass('canid', 'Canid', canid_level_tree, hit_die=8)


warrior_class = build_warrior_class()
thief_class = build_thief_class()
ranger_class = build_ranger_class()
canid_class = build_canid_class()

character_class_templates = {
    warrior_class.uid: warrior_class,
    thief_class.uid: thief_class,
    ranger_class.uid: ranger_class,
    canid_class.uid: canid_class
}
