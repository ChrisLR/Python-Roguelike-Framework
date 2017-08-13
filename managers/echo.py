from characters.enums import Sex
from enum import Enum
from collections import defaultdict
from components.game_object import NoneVoid


class EchoService(object):
    singleton = None

    def __init__(self, console, game_context):
        self.console = console
        self.game_context = game_context
        EchoService.singleton = self

    def _context_echo(self, message, **kwargs):
        context_variables = defaultdict(lambda: "N/A")
        context_variables["player"] = self.game_context.player

        for key, value in kwargs.items():
            if value:
                context_variables[key] = value

        for context_variable in context_variables.keys():
            if context_variable in message_router:
                context_variables[context_variable] = message_router[context_variable](**context_variables)

        for variable in MessageVariables:
            if variable.value in message and variable.name not in context_variables and variable.name in message_router:
                context_variables[variable.name] = message_router[variable.name](**context_variables)

        formatted_message = message.format(**context_variables)
        self.console.add_lines(formatted_message + "\n")

    def standard_context_echo(self, message, actor=None, target_item=None):
        self._context_echo(message, actor=actor, target_item=target_item)

    def combat_context_echo(self, message, attacker=None, defender=None,
                            attacker_weapon=None, defender_weapon=None, defender_bodypart=None):
        self._context_echo(
            message,
            attacker=attacker,
            defender=defender,
            attacker_weapon=attacker_weapon,
            defender_weapon=defender_weapon,
            defender_bodypart=defender_bodypart
        )


class MessageVariables(Enum):
    attacker = "{attacker}"
    attacker_weapon = "{attacker_weapon}"
    attacker_his = "{attacker_his}"
    attacker_him = "{attacker_him}"
    attacker_he = "{attacker_he}"
    defender = "{defender}"
    defender_his = "{defender_his}"
    defender_him = "{defender_him}"
    defender_he = "{defender_he}"
    defender_bodypart = "{defender_bodypart}"
    defender_armor = "{defender_armor}"
    defender_weapon = "{defender_weapon}"
    actor = "{actor}"
    target_item = "{target_item}"


def his_her_it(target, **kwargs):
    if 'player' in kwargs and kwargs['player'] == target:
        return "your"

    if hasattr(target, 'sex'):
        if target.sex == Sex.Male:
            return "his"
        if target.sex == Sex.Female:
            return "her"
    return "its"


def him_her_it(target, **kwargs):
    if 'player' in kwargs and kwargs['player'] == target:
        return "your"

    if hasattr(target, 'sex'):
        if target.sex == Sex.Male:
            return "him"
        if target.sex == Sex.Female:
            return "her"
    return "its"


def he_her_it(target, **kwargs):
    if 'player' in kwargs and kwargs['player'] == target:
        return "You"

    if hasattr(target, 'sex'):
        if target.sex == Sex.Male:
            return "he"
        if target.sex == Sex.Female:
            return "her"
    return "it"


def name_or_you(target, **kwargs):
    if 'player' in kwargs and kwargs['player'] == target:
        return "You"

    return target.name

none_void = NoneVoid()
# noinspection PyProtectedMember
message_router = {
    MessageVariables.attacker_his._name_: lambda **kwargs: his_her_it(target=kwargs["attacker"], **kwargs),
    MessageVariables.attacker_him._name_: lambda **kwargs: him_her_it(target=kwargs["attacker"], **kwargs),
    MessageVariables.attacker._name_: lambda **kwargs: name_or_you(target=kwargs["attacker"], **kwargs),
    MessageVariables.attacker_weapon._name_: lambda **kwargs: get_name_or_string(kwargs.get("attacker_weapon")),
    MessageVariables.attacker_he._name_: lambda **kwargs: he_her_it(target=kwargs.get("attacker")),
    MessageVariables.defender_his._name_: lambda **kwargs: his_her_it(target=kwargs["defender"], **kwargs),
    MessageVariables.defender_him._name_: lambda **kwargs: him_her_it(target=kwargs["defender"], **kwargs),
    MessageVariables.defender_he._name_: lambda **kwargs: he_her_it(target=kwargs.get("defender")),
    MessageVariables.defender._name_: lambda **kwargs: name_or_you(target=kwargs["defender"], **kwargs),
    MessageVariables.defender_weapon._name_: lambda **kwargs: get_name_or_string(kwargs.get("defender_weapon")),
    MessageVariables.defender_bodypart._name_: lambda **kwargs: get_name_or_string(kwargs.get("defender_bodypart")),
    MessageVariables.actor._name_: lambda **kwargs: get_name_or_string(kwargs.get("actor")),
    MessageVariables.target_item._name_: lambda **kwargs: get_name_or_string(kwargs.get("target_item")),
}


def get_name_or_string(value):
    if not value:
        return "None"
    if isinstance(value, str) or isinstance(value, int):
        return value
    else:
        return value.name


echo_service = None
