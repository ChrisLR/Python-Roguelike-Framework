import logging
import settings

from clubsandwich.ui import UIScene, ScrollingTextView, WindowView
from bearlibterminal import terminal

from areas.level import Level
from characters import actions
from data.python_templates.characters import character_templates
from data.python_templates.items import item_templates
from generators.dungeon_generator import DungeonGenerator
from generators.forerunner import Forerunner
from managers.action_manager import ActionManager
from managers.echo import EchoService
from scenes.game.windows import GameWindow, ItemQueryWindow, InventoryWindow, HudWindow
from clubsandwich.ui import LayoutOptions

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class GameScene(UIScene):
    """
    This handles everything relating to the UI in the game window.
    """
    ID = "Game"

    def __init__(self, game_context):
        self.console = ScrollingTextView(
            9, 110, layout_options=LayoutOptions(top=None, height=10, bottom=0, left=1, right=None, width=0.98))
        EchoService(self.console, game_context)
        game_context.action_manager = ActionManager(game_context)
        self.game_view = GameWindow(game_context, layout_options=LayoutOptions(top=10, height=30, bottom=None, left=0, right=None, width=1))
        self.game_context = game_context
        self.hud_view = HudWindow(game_context, layout_options=LayoutOptions(top=0, height=10, bottom=None, left=0, right=None, width=1))
        super().__init__(WindowView("", subviews=[self.hud_view, self.game_view, self.console]))
        self.loaded_levels = []

        # self.invoke_window(game_window)
        logger.info("Initialized GameScene")
        logger.info("Starting new game.")
        self.new_game()
        self.movement_keys = settings.KEY_MAPPINGS

    def terminal_read(self, val):
        # TODO It would be nice to only set moved=True if the action succeeded.
        player = self.game_context.player
        moved = False

        if player.is_dead():
            return

        if val is terminal.TK_KP_5 or val is terminal.TK_PERIOD:
            moved = True

        if val in self.movement_keys:
            key_x, key_y = self.movement_keys[val]
            self.game_context.action_manager.move_or_attack(player, key_x, key_y)
            moved = True

        if val is terminal.TK_I:
            self.director.push_scene(InventoryWindow(*self._get_all_player_items()))
            return

        if val is terminal.TK_D:
            self.director.push_scene(ItemQueryWindow(self._drop_item_callback, *self._get_all_player_items()))
            return

        if val is terminal.TK_E:
            self.director.push_scene(ItemQueryWindow(self._consume_item_callback, *self._get_all_player_items()))
            return

        if val is terminal.TK_G:
            for item in self.game_context.player.location.level.spawned_items:
                if item.location.get_local_coords() == self.game_context.player.location.get_local_coords():
                    actions.get(self.game_context.player, item)
            moved = True

        if val is terminal.TK_R:
            wielded_items, worn_items, _ = self._get_all_player_items()
            self.director.push_scene(ItemQueryWindow(self._remove_item_callback, wielded_items, worn_items, []))
            return

        if val is terminal.TK_W:
            self.director.push_scene(ItemQueryWindow(self._wear_wield_item_callback, *self._get_all_player_items()))
            return

        if moved:
            player.update()
            for monster in player.location.level.spawned_monsters:
                monster.update()
                self.game_context.action_manager.monster_take_turn(monster, player)

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
        player = self.game_context.player
        actions.consume(self.game_context.player, chosen_item)
        for monster in player.location.level.spawned_monsters:
            monster.update()
            self.game_context.action_manager.monster_take_turn(monster, player)

    def _drop_item_callback(self, chosen_item):
        player = self.game_context.player
        actions.drop(self.game_context.player, chosen_item)
        for monster in player.location.level.spawned_monsters:
            monster.update()
            self.game_context.action_manager.monster_take_turn(monster, player)

    def _wear_wield_item_callback(self, chosen_item):
        player = self.game_context.player
        actions.wear_wield(self.game_context.player, chosen_item)
        for monster in player.location.level.spawned_monsters:
            monster.update()
            self.game_context.action_manager.monster_take_turn(monster, player)

    def _remove_item_callback(self, chosen_item):
        player = self.game_context.player
        actions.remove_item(self.game_context.player, chosen_item)
        for monster in player.location.level.spawned_monsters:
            monster.update()
            self.game_context.action_manager.monster_take_turn(monster, player)

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
