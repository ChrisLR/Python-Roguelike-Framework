from characters.enums import Sex
from enum import Enum
from collections import defaultdict
from components.game_object import NoneVoid


class EchoService(object):
    # TODO This makes me cry, lets refactor this.
    singleton = None

    def __init__(self, console, game_context):
        self.console = console
        self.game_context = game_context
        if not EchoService.singleton:
            EchoService.singleton = self

    def standard_context_echo(self, message, actor=None, target_item=None):
        # TODO This is lame, refactor to reuse common code.
        context_variables = defaultdict(lambda: "N/A")
        context_variables["player"] = self.game_context.player

        if actor:
            context_variables["actor"] = actor
        if target_item:
            context_variables["target_item"] = target_item

        for context_variable in context_variables.keys():
            if context_variable in message_router:
                context_variables[context_variable] = message_router[context_variable](**context_variables)

        for variable in StandardMessageVariables:
            if variable.value in message and variable.name not in context_variables and variable.name in message_router:
                context_variables[variable.name] = message_router[variable.name](**context_variables)

        formatted_message = message.format(**context_variables)
        self.console.printStr(formatted_message + "\n")

    def combat_context_echo(self, message, attacker=None, defender=None,
                            attacker_weapon=None, defender_weapon=None, defender_bodypart=None):
        context_variables = defaultdict(lambda: "N/A")
        context_variables["player"] = self.game_context.player

        if attacker:
            context_variables["attacker"] = attacker
        if defender:
            context_variables["defender"] = defender
        if attacker_weapon:
            context_variables["attacker_weapon"] = attacker_weapon
        if defender_weapon:
            context_variables["defender_weapon"] = defender_weapon
        if defender_bodypart:
            context_variables["defender_bodypart"] = defender_bodypart

        for context_variable in context_variables.keys():
            if context_variable in message_router:
                context_variables[context_variable] = message_router[context_variable](**context_variables)

        for variable in CombatMessageVariables:
            if variable.value in message and variable.name not in context_variables and variable.name in message_router:
                context_variables[variable.name] = message_router[variable.name](**context_variables)

        formatted_message = message.format(**context_variables)
        self.console.printStr(formatted_message + "\n")


class CombatMessageVariables(Enum):
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


class StandardMessageVariables(Enum):
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
message_router = {
    CombatMessageVariables.attacker_his.name: lambda **kwargs: his_her_it(target=kwargs["attacker"], **kwargs),
    CombatMessageVariables.attacker_him.name: lambda **kwargs: him_her_it(target=kwargs["attacker"], **kwargs),
    CombatMessageVariables.attacker.name: lambda **kwargs: name_or_you(target=kwargs["attacker"], **kwargs),
    CombatMessageVariables.attacker_weapon.name: lambda **kwargs: kwargs.get("attacker_weapon", none_void).name,
    CombatMessageVariables.attacker_he.name: lambda **kwargs: he_her_it(target=kwargs.get("attacker")),
    CombatMessageVariables.defender_his.name: lambda **kwargs: his_her_it(target=kwargs["defender"], **kwargs),
    CombatMessageVariables.defender_him.name: lambda **kwargs: him_her_it(target=kwargs["defender"], **kwargs),
    CombatMessageVariables.defender_he.name: lambda **kwargs: he_her_it(target=kwargs.get("defender")),
    CombatMessageVariables.defender.name: lambda **kwargs: name_or_you(target=kwargs["defender"], **kwargs),
    CombatMessageVariables.defender_weapon.name: lambda **kwargs: kwargs.get("defender_weapon", none_void).name,
    CombatMessageVariables.defender_bodypart.name: lambda **kwargs: kwargs.get("defender_bodypart", none_void).name,
    StandardMessageVariables.actor.name: lambda **kwargs: kwargs.get("actor").name,
    StandardMessageVariables.target_item.name: lambda **kwargs: kwargs.get("target_item").name,
}
