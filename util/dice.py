import abc


class Dice(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def sides(self):
        pass


class D4(Dice):
    sides = 4


class D6(Dice):
    sides = 6


class D8(Dice):
    sides = 8


class D10(Dice):
    sides = 10


class D12(Dice):
    sides = 12


class D20(Dice):
    sides = 20


class DiceStack(object):
    __slots__ = ['amount', 'dice']

    def __init__(self, amount, dice):
        self.amount = amount
        self.dice = dice
