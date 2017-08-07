import cocos
import random

from areas.level import Level
from characters import actions
from data.python_templates.characters import character_templates
from data.python_templates.items import item_templates
from generators.dungeon_generator import DungeonGenerator
from generators.forerunner import Forerunner
from managers.action_manager import ActionManager
from managers.echo import EchoService
from scenes.game.layers import TilesLayer, ItemQueryWindow, InventoryWindow,ObjectLayer
import pyglet



class GameScene(cocos.scene.Scene):
    """
    This handles everything relating to the UI in the game window.
    """
    ID = "Game"
    def __init__(self, game_context):
        self.scroll_manager = cocos.layer.ScrollingManager()
        self.game_context = game_context
        self.new_game()
        self.tiles_layer = TilesLayer(game_context, self.scroll_manager)
        self.object_layer = ObjectLayer(game_context)
        self.scroll_manager.add(self.tiles_layer)
        self.scroll_manager.add(self.object_layer)
        super().__init__(self.scroll_manager)
        self.loaded_levels = []

        # game_context.action_manager = ActionManager(consoles[GameConsoles.ActionLog])
        # game_context.echo_service = EchoService(consoles[GameConsoles.ActionLog], game_context)
        #
        # game_window = GameWindow(console_manager.main_console, consoles, game_context)


    # def handle_input(self, key_events, mouse_events):
    #     if len(self.active_windows) > 1:
    #         super().handle_input(key_events, mouse_events)
    #         return
    #     super().handle_input(key_events, mouse_events)
    #
    #     for key_event in key_events:
    #         if key_event.keychar == "i":
    #             self.invoke_window(InventoryWindow(self.main_console, *self._get_all_player_items()))
    #
    #         if key_event.keychar == "d":
    #             self.invoke_window(
    #                 ItemQueryWindow(self.main_console, self._drop_item_callback, *self._get_all_player_items()))
    #
    #         if key_event.keychar == "e":
    #             self.invoke_window(
    #                 ItemQueryWindow(self.main_console, self._consume_item_callback, *self._get_all_player_items()))
    #
    #         if key_event.keychar == "g":
    #             for item in self.game_context.player.location.level.spawned_items:
    #                 if item.location.get_local_coords() == self.game_context.player.location.get_local_coords():
    #                     actions.get(self.game_context.player, item)
    #
    #         if key_event.keychar == "r":
    #             wielded_items, worn_items, _ = self._get_all_player_items()
    #             self.invoke_window(
    #                 ItemQueryWindow(self.main_console, self._remove_item_callback, wielded_items, worn_items, []))
    #
    #         if key_event.keychar == "w":
    #             self.invoke_window(
    #                 ItemQueryWindow(self.main_console, self._wear_wield_item_callback, *self._get_all_player_items()))

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

    def _drop_item_callback(self, chosen_item):
        actions.drop(self.game_context.player, chosen_item)

    def _wear_wield_item_callback(self, chosen_item):
        actions.wear_wield(self.game_context.player, chosen_item)

    def _remove_item_callback(self, chosen_item):
        actions.remove_item(self.game_context.player, chosen_item)

    def new_game(self):
        # TODO This should prepare the first level
        level = Level(width=80, height=45)
        level.name = "DEFAULT"
        level.min_room_size = 1
        level.max_room_size = 10
        level.max_rooms = 10
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

