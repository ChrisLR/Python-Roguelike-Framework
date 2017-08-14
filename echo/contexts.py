from echo import parameters
from echo import mutators
from echo import functions


class Context(object):
    __slots__ = ["parameters"]

    def __init__(self, *args):
        self.parameters = list(args)

    @classmethod
    def standard(cls, actor=None, target_item=None):
        return Context(parameters.Actor(actor), parameters.TargetItem(target_item))

    @classmethod
    def combat(cls, attacker=None, defender=None, attacker_weapon=None,
               defender_weapon=None, defender_bodypart=None, defender_armor=None):

        return Context(
            parameters.Attacker(attacker),
            parameters.Defender(defender),
            parameters.AttackerWeapon(attacker_weapon),
            parameters.DefenderWeapon(defender_weapon),
            parameters.DefenderBodypart(defender_bodypart),
            parameters.DefenderArmor(defender_armor),
        )

    def replace(self, message):
        for parameter in self.parameters:
            # No mutation
            if parameter.wildcard in message:
                message = message.replace(parameter.wildcard, functions.get_name_or_string(parameter.value))
            message = self._mutate_replace(message, parameter)

        return message

    def _mutate_replace(self, message, parameter):
        trimmed_wildcard = parameter.wildcard[1:-1:]
        if trimmed_wildcard in message:
            for mutator in mutators.listing:
                mutated_wildcard = "{}_{}".format("{" + trimmed_wildcard, mutator.suffix + "}")
                message = message.replace(mutated_wildcard, mutator.mutate(parameter.value))

        return message
