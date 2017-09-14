class AgeSet(object):
    __slots__ = ["adult_age", "elder_age", "maximum_age"]

    def __init__(self, adult_age, elder_age, maximum_age):
        self.adult_age = adult_age
        self.elder_age = elder_age
        self.maximum_age = maximum_age
