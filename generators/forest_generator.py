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


class ForestGenerator(object):
    """
        Takes a level config and outputs a new areas maze.
    """

    def __init__(self, factory_service):
        self.factory_service = factory_service
        self.forerunner = ForestForerunner

    def fill_with_grass(self, level):
        level.maze = [[tiles.forest_grass_floor.copy(x, y) for y in range(level.height)] for x in range(level.width)]

    def grow_big_trees(self, level):
        # We want about one big tree per 9 tile
        wanted_big_trees = int((level.width * level.height) / 9) + 1
        created = 0
        attempts = 0
        while created < wanted_big_trees:
            x = random.randrange(0, level.width)
            y = random.randrange(0, level.height)
            if self._verify_surroundings(level, x, y):
                level.maze[x][y] = tiles.forest_tree_wall.copy(x, y)
                created += 1
            else:
                attempts += 1
            if attempts > 100:
                break

    def _verify_surroundings(self, level, x, y):
        for x1 in range(0, 3):
            for y2 in range(0, 3):
                if x - (x1 - 1) in level.maze and y - (y2 - 1) in level.maze[x - (x1 -1)]:
                    if level.maze[x - (x1 - 1)][y - (y2 - 1)].uid == "forest_tree_wall":
                        return False
        return True

    def generate(self, level):
        """
        Generates a new areas based the level
        @param level: Level being generated
        @param player: Character controlled by the player
        """
        # TODO The dungeon's instances are spawned and loaded here.
        # fill map with "blocked" tiles
        self.fill_with_grass(level)
        self.grow_big_trees(level)


class ForestForerunner(object):
    """
    The Forerunner will traverse the forest and place forest objects such as monsters and items

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
        player_x = random.randrange(0, self.level.width)
        player_y = random.randrange(0, self.level.height)
        tile = self.level.maze[player_x][player_y]

        self._place_player(self.level, tile, self.player)

        self._place_monsters()
        # self.place_items_in_rooms()  # TODO
        # self.place_stairs(self.level.rooms)  # TODO

    def _place_monsters(self):
        if not self.level.monster_spawn_list:
            return
        for i in self.level.monster_spawn_list:
            x = random.randrange(0, self.level.width)
            y = random.randrange(0, self.level.height)

            tile = self.level.maze[x][y]
            self._place_monster(self.level, tile)

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
