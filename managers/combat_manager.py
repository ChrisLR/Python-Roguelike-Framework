import random

import echo.functions
from combat import attacks
from combat import defenses
from combat import enums as combat_enums
from combat import finishers
from managers.echo import EchoService
from stats.enums import StatsEnum
from util.colors import Colors

# TODO We are going the D&D 5E SRD route.
# TODO It still means we can have several attack flavors and defense flavors
# TODO But we should streamline the actual attacks.
all_attacks = (attacks.MeleeAttack, attacks.Punch)
all_ranged_attacks = (attacks.FireWeapon, )
all_defenses = (defenses.ArmorAbsorb, defenses.Block, defenses.Dodge, defenses.Miss, defenses.Parry)
all_finishers = (finishers.Impale, finishers.ChokePunch, finishers.CrushSkull)


def choose_attack(attacker, defender, ranged=False):
    if ranged:
        possible_attacks = [attack for attack in all_ranged_attacks if attack.can_execute(attacker, defender)]
    else:
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


def execute_combat_round(attacker, defender, ranged=False):
    """
    This is meant to be the "round" when you walk into someone.
    """
    # Prepare attack
    attack_template = choose_attack(attacker, defender, ranged)
    if not attack_template:
        return

    attack_results = attack_template.execute(attacker, defender)
    if not attack_results:
        return

    for attack_result in attack_results:
        attack_result.attack_used = attack_template
        threat_level = get_threat_level(attack_result.total_damage, defender.stats.get_current_value(StatsEnum.Health))
        attack_result.body_part_hit = defender.body.get_random_body_part_for_threat_level(threat_level)
        death = False
        if attack_result.success:
            damage_string, death, finisher = take_damage(defender, attack_result)
            if finisher:
                message = "{}\n".format(damage_string)
            else:
                message = "{}, {}\n".format(attack_result.attack_message, damage_string)
        else:
            defense_result = choose_defense(attack_result).execute(attack_result)
            message = "{}, {}\n".format(attack_result.attack_message, defense_result.message)

        EchoService.singleton.echo(message)
        EchoService.singleton.echo(str(attack_result))
        if death:
            if defender.is_player:
                player_death(defender)
            else:
                monster_death(defender)
            x, y = defender.location.get_local_coords()
            defender.current_level.maze[x][y].contains_object = False
            return


def take_damage(actor, attack_result):
    # TODO Here we take each damage dealt, apply resistance
    # TODO Determine threat level for total damage
    if attack_result.total_damage <= 0:
        return "to no effect.", False, False
    damage_string = ""
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

    is_killing_blow = False
    is_finisher = False
    # check for death. if there's a death function, call it
    if actor.stats.get_current_value(StatsEnum.Health) <= 0:
        is_killing_blow = True
        if random.randint(0, 10) <= 10:
            # Here, instead of displaying the damage, we try to execute a finisher.
            possible_finishers = [finisher for finisher in all_finishers if finisher.evaluate(attack_result)]
            if possible_finishers:
                is_finisher = True
                finisher = random.choice(possible_finishers)
                damage_string = finisher.execute(attack_result)
                return damage_string, is_killing_blow, is_finisher
        return damage_string, is_killing_blow, is_finisher
    return damage_string, is_killing_blow, is_finisher


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

