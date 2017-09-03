class LevelTree(object):
    NAME = "level_tree"
    """
    The goal of this Tree is to return advantages of a level recursively.
    """
    def __init__(self, stats_modifiers=None, ability_modifiers=None, mutations=None):
        super().__init__()
        self.stats_modifiers = stats_modifiers if stats_modifiers else {}
        self.ability_modifiers = ability_modifiers if ability_modifiers else {}
        self.mutations = mutations if mutations else {}

    def get_stat_modifiers(self, current_level):
        final_modifiers = {}
        ordered_modifiers = sorted(self.stats_modifiers.keys())
        for level in ordered_modifiers:
            if int(level) > int(current_level):
                continue

            for stat_modifier in self.stats_modifiers[level]:
                if stat_modifier in final_modifiers:
                    final_modifiers[stat_modifier.uid] += stat_modifier.get_leveled_value(current_level, level)
                else:
                    final_modifiers[stat_modifier.uid] = stat_modifier.get_leveled_value(current_level, level)

        return final_modifiers

    def get_ability_modifiers(self, current_level):
        final_modifiers = {}
        for level in sorted(self.ability_modifiers.keys()):
            if level > current_level:
                continue
            for ability_modifier in self.ability_modifiers[level]:
                if ability_modifier.uid in final_modifiers:
                    final_modifiers[ability_modifier.uid] += ability_modifier.get_leveled_value(current_level, level)
                else:
                    final_modifiers[ability_modifier.uid] = ability_modifier.get_leveled_value(current_level, level)

        return final_modifiers

    def add_stat_modifier(self, level, stat_modifier):
        if level not in self.stats_modifiers:
            self.stats_modifiers[level] = []
        self.stats_modifiers[level].append(stat_modifier)

    def add_ability_modifier(self, level, ability_modifier):
        if level not in self.ability_modifiers:
            self.ability_modifiers[level] = []
        self.ability_modifiers[level].append(ability_modifier.power)

    def add_mutation(self, level, mutation):
        if level not in self.mutations:
            self.mutations[level] = []
        self.mutations[level].append(mutation)

    def get_mutations_for_level(self, level):
        """
        This returns the mutations for a single level, not recursive.
        :param level: Level requested.
        :return: Mutations iterable
        """
        return self.mutations.get(level, None)






