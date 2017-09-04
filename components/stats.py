from components.component import Component
from stats import Stat, StatsEnum
from stats.enums import Size
import copy

class CharacterStats(Component):
    NAME = 'stats'
    """
    This is the component that implements D&D stats.
    """

    def __init__(self, base_ability_score_set, size=Size.Medium):
        super().__init__()
        self.base_ability_score_set = base_ability_score_set
        self.registered_modifiers = {
            StatsEnum.Strength: [],
            StatsEnum.Dexterity: [],
            StatsEnum.Constitution: [],
            StatsEnum.Intelligence: [],
            StatsEnum.Wisdom: [],
            StatsEnum.Charisma: [],
            StatsEnum.Size: [],
        }
        self.base_size = size

    @property
    def strength(self):
        modifiers = self.registered_modifiers[StatsEnum.Strength]
        return Stat(self.base_ability_score_set.strength + sum(modifiers))

    @property
    def dexterity(self):
        modifiers = self.registered_modifiers[StatsEnum.Dexterity]
        return Stat(self.base_ability_score_set.dexterity + sum(modifiers))

    @property
    def constitution(self):
        modifiers = self.registered_modifiers[StatsEnum.Constitution]
        return Stat(self.base_ability_score_set.constitution + sum(modifiers))

    @property
    def intelligence(self):
        modifiers = self.registered_modifiers[StatsEnum.Intelligence]
        return Stat(self.base_ability_score_set.intelligence + sum(modifiers))

    @property
    def wisdom(self):
        modifiers = self.registered_modifiers[StatsEnum.Wisdom]
        return Stat(self.base_ability_score_set.wisdom + sum(modifiers))

    @property
    def charisma(self):
        modifiers = self.registered_modifiers[StatsEnum.Charisma]
        return Stat(self.base_ability_score_set.charisma + sum(modifiers))

    @property
    def size(self):
        modifiers = self.registered_modifiers[StatsEnum.Size]
        return Stat(self.base_size + sum(modifiers))

    def register_modifier(self, stat_modifier):
        self.registered_modifiers[stat_modifier.stat_enum].append(stat_modifier)

    def unregister_modifier(self, stat_modifier):
        self.registered_modifiers[stat_modifier.stat_enum].remove(stat_modifier)

    def copy(self):
        return CharacterStats(copy.copy(self.base_ability_score_set))
