import abc


class Race(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def uid(self):
        pass

    @abc.abstractclassmethod
    def name(self):
        pass

    @abc.abstractclassmethod
    def ability_score_adjustments(self):
        pass

    @abc.abstractclassmethod
    def age_set(self):
        pass

    @abc.abstractclassmethod
    def alignment_set(self):
        pass

    @abc.abstractclassmethod
    def size(self):
        pass

    @abc.abstractclassmethod
    def average_height(self):
        pass

    @abc.abstractclassmethod
    def average_weight(self):
        pass

    @abc.abstractclassmethod
    def speed(self):
        pass

    @abc.abstractclassmethod
    def skill_proficiencies(self):
        pass

    @abc.abstractclassmethod
    def known_languages(self):
        pass

    @abc.abstractclassmethod
    def body(self):
        pass

    @abc.abstractclassmethod
    def racial_powers(self):
        pass
