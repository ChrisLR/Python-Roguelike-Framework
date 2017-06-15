import logging
import random

from areas.level import Level
from base.scene import BaseScene
from characters import actions
from data.python_templates.characters import character_templates
from data.python_templates.items import item_templates
from generators.dungeon_generator import DungeonGenerator
from managers.action_manager import ActionManager
from managers.echo import EchoService
from scenes.game.windows import GameWindow, ItemQueryWindow, InventoryWindow
from scenes.game.windows.game_window import GameConsoles

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class GameScene(BaseScene):
    """
    This handles everything relating to the UI in the game window.
    """
    ID = "Game"

    def __init__(self, console_manager, scene_manager, game_context):
        super().__init__(console_manager, scene_manager, game_context)
        self.loaded_levels = []
        consoles = {
            GameConsoles.ActionLog: self.console_manager.create_new_console(80, 15),
            GameConsoles.Status: self.console_manager.create_new_console(20, 15)
        }
        game_context.action_manager = ActionManager(consoles[GameConsoles.ActionLog])
        game_context.echo_service = EchoService(consoles[GameConsoles.ActionLog], game_context)

        game_window = GameWindow(console_manager.main_console, consoles, game_context)
        self.invoke_window(game_window)
        logger.info("Initialized GameScene")
        logger.info("Starting new game.")
        self.new_game()

    def handle_input(self, key_events, mouse_events):
        if len(self.active_windows) > 1:
            super().handle_input(key_events, mouse_events)
            return
        super().handle_input(key_events, mouse_events)

        for key_event in key_events:
            if key_event.keychar == "i":
                self.invoke_window(InventoryWindow(self.main_console, *self._get_all_player_items()))

            if key_event.keychar == "d":
                self.invoke_window(
                    ItemQueryWindow(self.main_console, self._drop_item_callback, *self._get_all_player_items()))

            if key_event.keychar == "e":
                self.invoke_window(
                    ItemQueryWindow(self.main_console, self._consume_item_callback, *self._get_all_player_items()))

            if key_event.keychar == "g":
                for item in self.game_context.player.location.level.spawned_items:
                    if item.location.get_local_coords() == self.game_context.player.location.get_local_coords():
                        actions.get(self.game_context.player, item)

            if key_event.keychar == "r":
                wielded_items, worn_items, _ = self._get_all_player_items()
                self.invoke_window(
                    ItemQueryWindow(self.main_console, self._remove_item_callback, wielded_items, worn_items, []))

            if key_event.keychar == "w":
                self.invoke_window(
                    ItemQueryWindow(self.main_console, self._wear_wield_item_callback, *self._get_all_player_items()))

    def _get_all_player_items(self):
        player = self.game_context.player
        wielded_items = []
        worn_items = []
        inventory_items = []
        if player.equipment:
            wielded_items = player.equipment.get_wielded_items()
            worn_items = player.equipment.get_worn_items()

        if player.inventory:
            inventory_items = player.inventory.get_all_items()

        return wielded_items, worn_items, inventory_items

    def _consume_item_callback(self, chosen_item):
        actions.consume(self.game_context.player, chosen_item)
        self.close_window()

    def _drop_item_callback(self, chosen_item):
        actions.drop(self.game_context.player, chosen_item)
        self.close_window()

    def _wear_wield_item_callback(self, chosen_item):
        actions.wear_wield(self.game_context.player, chosen_item)
        self.close_window()

    def _remove_item_callback(self, chosen_item):
        actions.remove_item(self.game_context.player, chosen_item)
        self.close_window()

    def new_game(self):
        # TODO This should prepare the first level
        level = Level()
        level.name = "DEFAULT"
        level.min_room_size = 1
        level.max_room_size = 10
        level.max_rooms = 10
        level.width = 80
        level.height = 45
        self.init_dungeon(level)

    def init_dungeon(self, level):
        dungeon_generator = DungeonGenerator(self.game_context.factory_service)
        player = self.game_context.player
        player.is_player = True
        dungeon_generator.generate(level)
        self.place_dungeon_objects(level, player)

    def place_dungeon_objects(self, level, player):
        character_factory = self.game_context.character_factory
        item_factory = self.game_context.item_factory
        level.monster_spawn_list = [character_factory.build(uid) for uid, monster in character_templates.items()]
        level.item_spawn_list = [item_factory.build(uid) for uid, item in item_templates.items()]

        forerunner = Forerunner(level, player)
        forerunner.run()




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
            logger.debug("Could not find appropriate tile to spawn items.")
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

