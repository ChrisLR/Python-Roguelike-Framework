import random

from combat import enums as combat_enums
from combat import attacks
from combat import defenses
from echo.contexts import Context
from stats.enums import StatsEnum
from managers.echo import EchoService
import echo.functions
from util.colors import Colors


# TODO We are going the D&D 5E SRD route.
# TODO It still means we can have several attack flavors and defense flavors
# TODO But we should streamline the actual attacks.
all_attacks = (attacks.MeleeAttack, attacks.Punch)
all_defenses = (defenses.ArmorAbsorb, defenses.Block, defenses.Dodge, defenses.Miss, defenses.Parry)


def choose_attack(attacker, defender):
    possible_attacks = [attack for attack in all_attacks if attack.can_execute(attacker, defender)]

    # TODO These attacks should have a priority by effectiveness
    # TODO They should also apply their prereqs
    if possible_attacks:
        if attacks.MeleeAttack in possible_attacks:
            return attacks.MeleeAttack
        else:
            return random.choice(possible_attacks)


def choose_defense(attack_result):
    possible_defenses = [defense for defense in all_defenses if defense.evaluate(attack_result)]

    return random.choice(possible_defenses)


def execute_combat_round(attacker, defender):
    """
    This is meant to be the "round" when you walk into someone.
    """
    # Prepare attack
    attack_template = choose_attack(attacker, defender)
    if not attack_template:
        return
    attack_results = attack_template.execute(attacker, defender)
    for attack_result in attack_results:
        EchoService.singleton.echo(attack_result.attack_message + "...\n")
        threat_level = get_threat_level(attack_result.total_damage, defender.stats.get_current_value(StatsEnum.Health))
        attack_result.body_part_hit = defender.body.get_random_body_part_for_threat_level(threat_level)
        if attack_result.success:
            # TODO We might want to display info about actual rolls but that should be handled in the Echo manager/service
            # TODO I am still unsure on where its best to apply actual damage.
            # TODO Leaving it in the defender object could have them behave differently
            # TODO but at the same time having it centralized in one location will keep the other classes smaller.
            # TODO Maybe this should be extracted to a component?
            take_damage(defender, attack_result)
        else:
            defense_result = choose_defense(attack_result).execute(attack_result)
            EchoService.singleton.echo("...{}\n".format(defense_result.message))

        EchoService.singleton.echo(str(attack_result) + "\n")


def take_damage(actor, attack_result):
    # TODO Here we take each damage dealt, apply resistance
    # TODO Determine threat level for total damage
    if attack_result.total_damage <= 0:
        return
    damage_string = "... "
    wound_strings = []

    for damage, damage_type in attack_result.separated_damage:
        if damage > 0:
            wound_strings.append(describe_wounds(damage_type))
            actor.stats.modify_core_current_value(StatsEnum.Health, -damage)

    damage_string += ",".join(wound_strings)
    damage_string += " {} {} for {} damage!".format(
        echo.functions.his_her_it(actor),
        attack_result.body_part_hit.name,
        attack_result.total_damage
    )
    EchoService.singleton.echo(damage_string + "\n")

    # TODO THIS MUST BE EXTRACTED
    # check for death. if there's a death function, call it
    if actor.stats.get_current_value(StatsEnum.Health) <= 0:
        if actor.is_player:
            player_death(actor)
        else:
            monster_death(actor)

        x, y = actor.location.get_local_coords()
        actor.current_level.maze[x][y].contains_object = False


def player_death(player):
    # TODO This should not be here
    # the game ended!
    EchoService.singleton.echo('You have died... Game Over\n\n')

    # for added effect, transform the player into a corpse!
    player.display.ascii_character = '%'
    player.display.foreground_color = Colors.CRIMSON


def monster_death(monster):
    # TODO This should not be here
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    EchoService.singleton.echo('{} has died.\n\n'.format(monster.name))
    monster.display.ascii_character = '%'
    monster.display.foreground_color = Colors.CRIMSON
    monster.blocks = False
    monster.name = 'remains of ' + monster.name


def get_threat_level(total_damage, health):
    minor = (float(health) / 5)
    major = (float(health) / 2.5)
    critical = (float(health) / 1.5)

    if total_damage <= minor:
        return combat_enums.ThreatLevel.Minor
    elif minor < total_damage <= major:
        return combat_enums.ThreatLevel.Major
    elif major < total_damage <= health:
        return combat_enums.ThreatLevel.Critical
    elif total_damage >= health:
        return combat_enums.ThreatLevel.Fatal


def describe_wounds(damage_type):
    if damage_type == combat_enums.DamageType.Blunt:
        return "bruising"
    elif damage_type == combat_enums.DamageType.Slash:
        return "cutting"
    elif damage_type == combat_enums.DamageType.Pierce:
        return "piercing"

# TODO Implement Limb Damaging statuses.

