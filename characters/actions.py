"""
Action commands

This is where the main business logic lives.

Any action that can be taken by the player or a npc (e.g. monster) is defined here.
"""
import math

from managers import combat_manager, echo
from components.location import Location
from components.messages import MessageType, QueryType
from cocos import actions


# TODO One thing I want to change is the tile contains flag
# TODO It should not have to be changed EVERY time something moves, instead we should
# TODO Abstract it to another layer which would handle WHATEVER it needs to move something
# TODO Because many actions will move characters and not all of them will make it "walk"
# TODO also because it only take one forgotten line to make difficult to track bugs.


def attack(attacker, target, console):
    # a simple formula for attack damage
    combat_manager.execute_combat_round(attacker, target)


def consume(actor, chosen_item):
    if chosen_item.consumable:
        actor.transmit_query(None, QueryType.RemoveObject, item=chosen_item)
        chosen_item.consumable.consume(actor)
    else:
        echo.EchoService.singleton.standard_context_echo("You can't eat that!")


def drop(actor, chosen_item):
    chosen_item.register_component(actor.location.copy())
    if True in actor.transmit_query(None, QueryType.RemoveObject, item=chosen_item):
        actor.location.level.spawned_items.append(chosen_item)
        echo.EchoService.singleton.standard_context_echo("{actor} drop {chosen_item}.", actor, chosen_item)


def get(actor, chosen_item):
    # TODO Inventories will have a maximum and this will need to prevent the drop.
    actor.inventory.add_item(chosen_item)
    actor.location.level.spawned_items.remove(chosen_item)
    chosen_item.unregister_component_name(Location.NAME)
    echo.EchoService.singleton.standard_context_echo("{actor} get {target_item}.", actor, chosen_item)


def remove_item(actor, chosen_item):
    if True in actor.transmit_query(None, QueryType.RemoveObject, item=chosen_item):
        actor.inventory.add_item(chosen_item)
        echo.EchoService.singleton.standard_context_echo(
            "{actor} remove {target_item}.", actor, chosen_item)


def wear_wield(actor, chosen_item):
    success = False
    if chosen_item.armor and actor.equipment:
        if actor.equipment.wear(chosen_item):
            echo.EchoService.singleton.standard_context_echo(
                "{actor} wear {target_item}.", actor, chosen_item)
    elif actor.equipment:
        if actor.equipment.wield(chosen_item):
            echo.EchoService.singleton.standard_context_echo(
                "{actor} wield {target_item}.", actor, chosen_item)
            success = True

    if success:
        actor.inventory.remove_item(chosen_item)
    else:
        echo.EchoService.singleton.standard_context_echo("You can't wear/wield that!")


def move(actor, dx, dy):

    x, y = actor.location.get_local_coords()
    new_x = x + dx
    new_y = y + dy

    old_tile = actor.current_level.tiles[x][y].tile
    new_tile = actor.current_level.tiles[new_x][new_y].tile

    # move by the given amount, if the destination is not blocked
    if not new_tile.is_blocked:
        # TODO This kind of is blocked causes bugs where an actor moves somewhere an actor dies.
        # TODO makes it impossible to auto attack on that tile.
        actor.location.local_x = new_x
        actor.location.local_y = new_y
        old_tile.contains_object = False
        new_tile.contains_object = True
        if actor.cocos:
            actor.cocos.do(actions.MoveTo((new_x, new_y), duration=0.1))


def distance_to(actor, target):
    # TODO This should not be here
    actor_x, actor_y = actor.location.get_local_coords()
    target_x, target_y = target.location.get_local_coords()

    # return the distance to another object
    distance_x = target_x - actor_x
    distance_y = target_y - actor_y
    return math.sqrt(distance_x ** 2 + distance_y ** 2)


def move_or_attack(character, target_x, target_y, console):
    """
    Either move to a new tile or attack
    whatever is in your way.
    """
    # the coordinates the player is moving to/attacking
    x = character.location.local_x
    y = character.location.local_y
    new_x = x + target_x
    new_y = y + target_y
    new_tile = character.current_level.tiles[new_x][new_y].tile

    # try to find an attack-able object there
    if new_tile.contains_object:
        tile_coords = new_tile.location.get_local_coords()
        monster = next((monster for monster in character.current_level.spawned_monsters
                        if monster.location.get_local_coords() == tile_coords), None)
        if monster:
            attack(character, monster, console)
    else:
        move(character, target_x, target_y)


def move_towards(actor, target):
    # TODO I think this should be split,  a part that determines in which direction you have to move
    # TODO then reuse the part where we try to move instead.
    # TODO Because we will be able to reuse it for missiles/spells
    actor_x, actor_y = actor.location.get_local_coords()
    target_x, target_y = target.location.get_local_coords()
    # vector from this object to the target, and distance
    distance_x = target_x - actor_x
    distance_y = target_y - actor_y
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    # normalize it to length 1 (preserving direction), then round it and
    # convert to integer so the movement is restricted to the map grid
    distance_x = int(round(distance_x / distance))
    distance_y = int(round(distance_y / distance))
    move(actor, distance_x, distance_y)


def monster_take_turn(monster, player, console):
    # TODO This should not be here, it should be in an AI component which uses actions from here
    """
    A basic monster takes its turn.9
    If you can see it, it can see you
    """
    if not monster.is_dead():
        x, y = monster.location.get_local_coords()
        if (x, y) in player.fov:
            # move towards player if far away
            if distance_to(monster, player) >= 2:
                move_towards(monster, player)
            # close enough, attack! (if the player is still alive.)
            elif not player.is_dead():
                attack(monster, player, console)
