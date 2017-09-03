import math


class Stat(object):
    def __init__(self, uid, current, maximum):
        self.uid = uid
        self.current = current
        self.maximum = maximum

    def __str__(self):
        return str(self.current)

    def __int__(self):
        return int(self.current)

    def modify_current(self, value):
        self.current += value

    def modify_max(self, value):
        self.maximum += value


class StatModifier(object):
    def __init__(self, stat_enum, value):
        self.stat_enum = stat_enum
        self.value = value

    def __int__(self):
        return self.value


