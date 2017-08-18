from characters.enums import Sex


def his_her_it(value):
    if hasattr(value, "is_player") and value.is_player:
        return "your"

    if hasattr(value, 'sex'):
        if value.sex == Sex.Male:
            return "his"
        if value.sex == Sex.Female:
            return "her"
    return "its"


def him_her_it(value):
    if hasattr(value, "is_player") and value.is_player:
        return "you"

    if hasattr(value, 'sex'):
        if value.sex == Sex.Male:
            return "him"
        if value.sex == Sex.Female:
            return "her"
    return "its"


def he_her_it(value):
    if hasattr(value, "is_player") and value.is_player:
        return "you"

    if hasattr(value, 'sex'):
        if value.sex == Sex.Male:
            return "he"
        if value.sex == Sex.Female:
            return "her"
    return "it"


def name_or_you(value):
    if hasattr(value, "is_player") and value.is_player:
        return "you"

    return value.name


def names_or_your(value):
    if hasattr(value, "is_player") and value.is_player:
        return "your"

    return value.name + "'s"


def get_name_or_string(value):
    if not value:
        return "None"
    if isinstance(value, str) or isinstance(value, int):
        return value
    else:
        return value.name
