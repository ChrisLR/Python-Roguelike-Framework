import logging
import random

from areas.room import Room
from areas.tile import Tile
from data.python_templates import tiles

logger_ = logging.getLogger("generator")
logger_.addHandler(logging.StreamHandler())

"""
We will want to have many generators, as template we could start with
World Generator, Dungeon Generator, Wilderness Generator.
"""


class DungeonGenerator(object):
    """
        Takes a level config and outputs a new areas maze.
    """

    def __init__(self, factory_service):
        self.factory_service = factory_service
        self.forerunner = Forerunner

    @staticmethod
    def _create_room(level, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                level.maze[x][y] = tiles.dirt_floor.copy(x, y)

    @staticmethod
    def _create_h_tunnel(level, x1, x2, y):
        # horizontal tunnel. min() and max() are used in case x1>x2
        for x in range(min(x1, x2), max(x1, x2) + 1):
            level.maze[x][y] = tiles.dirt_floor.copy(x, y)

    @staticmethod
    def _create_v_tunnel(level, y1, y2, x):
        # vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            level.maze[x][y] = tiles.dirt_floor.copy(x, y)

    def generate(self, level):
        """
        Generates a new areas based the level
        @param level: Level being generated
        @param player: Character controlled by the player
        """
        # TODO The dungeon's instances are spawned and loaded here.
        # fill map with "blocked" tiles
        level.maze = [[tiles.dirt_wall.copy(x, y) for y in range(level.height)] for x in range(level.width)]

        for r in range(level.max_rooms):
            # random width and height
            w = random.randint(level.min_room_size, level.max_room_size)
            h = random.randint(level.min_room_size, level.max_room_size)

            # random position without going out of the boundaries of the map
            x = random.randint(0, level.width - w - 1)
            y = random.randint(0, level.height - h - 1)

            # "DungeonRoom" class makes rectangles easier to work with
            new_room = Room(x, y, w, h)
            level.rooms.append(new_room)

            # run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in level.rooms:
                if other_room is not new_room and new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self._create_room(level, new_room)

                # center coordinates of new room, will be useful later
                new_x, new_y = new_room.center()

                if level.num_rooms > 0:
                    # connect it to the previous room with a tunnel
                    # center coordinates of previous room
                    (prev_x, prev_y) = level.rooms[level.num_rooms - 1].center()

                    # draw a coin (random number that is either 0 or 1)
                    if random.randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self._create_h_tunnel(level, prev_x, new_x, prev_y)
                        self._create_v_tunnel(level, prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self._create_v_tunnel(level, prev_y, new_y, prev_x)
                        self._create_h_tunnel(level, prev_x, new_x, new_y)

                # finally, append the new room to the list
                level.rooms.append(new_room)
                level.num_rooms += 1

        # connect them with a tunnel
        self._create_h_tunnel(level, 25, 55, 23)


class Forerunner(object):
    """
    The Forerunner will traverse the dungeon and place dungeon objects such as monsters and items

    Usage:
        forerunner = Forefunner(level, player)
        forerunner.run()
    """
    # TODO: figure out someplace besides scene.py where this should live

    def __init__(self, level, player):
        self.level = level
        self.player = player

    def run(self):
        # place the player in the center of the first room
        first_room = self.level.rooms[0]
        x, y = first_room.center()
        tile = self.level.maze[x][y]
        self._place_player(self.level, tile, self.player)

        self._place_monsters_in_rooms()
        # self.place_items_in_rooms()  # TODO
        # self.place_stairs(self.level.rooms)  # TODO

    def _get_random_room_tile(self, level, room, depth=0):
        """
        Get a random ground tile that does not already contain a object
        @param level: Level being generated.
        @param depth: This prevents crash by infinite recursion.
        @param room:
        @return:
        """
        if room.x1 + 1 < room.x2 - 1:
            x = random.randint(room.x1 + 1, room.x2 - 1)
        else:
            x = room.x1 + 1

        if room.y1 + 1 < room.y2 - 1:
            y = random.randint(room.y1 + 1, room.y2 - 1)
        else:
            y = room.y1 + 1

        tile = level.maze[x][y]

        if not tile.contains_object:
            return tile

        if depth > 50:
            return tile

        # if we didn't find an empty tile, try again
        return self._get_random_room_tile(level, room, depth=depth + 1)

    def _place_monsters_in_rooms(self):
        """
        Go through each room (thats not the first one) and drop a monster in it. Keep
        going until there are no more monsters to place.
        """
        for room in self.level.rooms[1:]:
            if not self.level.monster_spawn_list:
                break
            tile = self._get_random_room_tile(self.level, room)
            self._place_monster(self.level, tile)

    def _place_items_in_rooms(self):
        """
        Go through each room (thats not the first one) and drop an items in it. Keep
        going until there are no more items to place.
        """
        for item in self.level.item_spawn_list:
            random_room = random.choice(self.level.rooms[1:])
            tile = self._get_random_room_tile(self.level, random_room)
            self._place_item(self.level, tile, item)

    @staticmethod
    def _place_monster(level, tile):
        # TODO This kind of spawning has a few issues, it should use a service to spawn monsters.
        monster = level.monster_spawn_list.pop(0)
        monster.location = tile.location.copy()
        monster.location.level = level
        level.spawned_monsters.append(monster)
        tile.contains_object = True

    @staticmethod
    def _place_player(level, tile, player):
        """
        Place the player in the maze.
        """
        player.location = tile.location.copy()
        player.location.level = level
        tile.contains_object = True

    @staticmethod
    def _place_item(level, tile, item):
        # TODO This sort of assignment should use a method and set all required things like global x, area, etc
        item.location.local_x = tile.x
        item.location.local_y = tile.y
        item.level = level

    def _place_stairs(self, tile):
        # TODO Stairs should not be an item but a passable tile.
        pass
