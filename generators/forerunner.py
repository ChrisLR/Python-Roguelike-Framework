import random


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
        tile = self.level.tiles[x][y]
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

        cell = level.tiles[x][y]

        if not cell.tile.contains_object:
            return cell

        if depth > 50:
            return cell

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
    def _place_monster(level, cell):
        # TODO This kind of spawning has a few issues, it should use a service to spawn monsters.
        monster = level.monster_spawn_list.pop(0)
        monster.location = cell.tile.location.copy()
        monster.location.level = level
        level.spawned_monsters.append(monster)
        cell.tile.contains_object = True
        level.object_cell_grid.place(monster, cell.i, cell.j)

    @staticmethod
    def _place_player(level, cell, player):
        """
        Place the player in the tiles.
        """
        player.location = cell.tile.location.copy()
        player.location.level = level
        cell.tile.contains_object = True
        level.object_cell_grid.place(player, cell.i, cell.j)

    @staticmethod
    def _place_item(level, tile, item):
        # TODO This sort of assignment should use a method and set all required things like global x, area, etc
        item.location.local_x = tile.x
        item.location.local_y = tile.y
        item.level = level
        level.object_cell_grid.place(item, tile.x, tile.y)

    def _place_stairs(self, tile):
        # TODO Stairs should not be an item but a passable tile.
        pass
