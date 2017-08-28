class AbilityScoreSet(object):
    __slots__ = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

    def __init__(self, strength=0, dexterity=0, constitution=0, intelligence=0, wisdom=0, charisma=0):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

    @classmethod
    def set_all(cls, value):
        return AbilityScoreSet(
            strength=value,
            dexterity=value,
            constitution=value,
            intelligence=value,
            wisdom=value,
            charisma=value
        )
