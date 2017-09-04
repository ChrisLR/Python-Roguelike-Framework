from stats import StatsEnum, StatModifier, StatModifierType


class AbilityScoreSet(object):
    __slots__ = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "_modifiers"]

    def __init__(self, strength=0, dexterity=0, constitution=0, intelligence=0, wisdom=0, charisma=0):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

        self._modifiers = [
            modifier for modifier in (
                StatModifier(StatsEnum.Strength, self.strength, StatModifierType.Racial),
                StatModifier(StatsEnum.Dexterity, self.dexterity, StatModifierType.Racial),
                StatModifier(StatsEnum.Constitution, self.constitution, StatModifierType.Racial),
                StatModifier(StatsEnum.Intelligence, self.intelligence, StatModifierType.Racial),
                StatModifier(StatsEnum.Wisdom, self.wisdom, StatModifierType.Racial),
                StatModifier(StatsEnum.Charisma, self.charisma, StatModifierType.Racial),
            ) if modifier != 0
        ]

    @property
    def as_modifiers(self):
        return self._modifiers

    @classmethod
    def set_all(cls, value, **kwargs):
        return AbilityScoreSet(
            strength=kwargs.get("strength", value),
            dexterity=kwargs.get("dexterity", value),
            constitution=kwargs.get("constitution", value),
            intelligence=kwargs.get("intelligence", value),
            wisdom=kwargs.get("wisdom", value),
            charisma=kwargs.get("charisma", value)
        )
