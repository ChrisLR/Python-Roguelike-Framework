import abc
from abilities.base import Ability
from managers.echo import EchoService


# noinspection PyTypeChecker,PyAbstractClass
class PhysicalAbility(Ability):
    __metaclass__ = abc.ABCMeta

    @classmethod
    def on_loss(cls, actor):
        EchoService.singleton.player_echo(actor, "You lose your ability to " + cls.name)

    @classmethod
    def on_gain(cls, actor):
        EchoService.singleton.player_echo(actor, "You gain the ability to " + cls.name)


class Breathe(PhysicalAbility):
    name = "Breathe"
    is_passive = True
    is_stackable = False


class Eat(PhysicalAbility):
    name = "Eat"
    is_passive = True
    is_stackable = False


class Grasp(PhysicalAbility):
    name = "Grasp"
    is_passive = True
    is_stackable = False


class Think(PhysicalAbility):
    name = "Think"
    is_passive = True
    is_stackable = True








