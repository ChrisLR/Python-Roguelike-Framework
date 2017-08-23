import logging

from bearlibterminal import terminal
from clubsandwich.ui import LayoutOptions
from clubsandwich.ui import UIScene, ScrollingTextView, WindowView
import random
import settings
from areas.level import Level
from characters import actions
from data.python_templates.characters import character_templates
from data.python_templates.items import item_templates
from generators import dungeon_generator, forest_generator
from managers.action_manager import ActionManager
from managers.echo import EchoService
from scenes.game.windows import GameWindow, ItemQueryWindow, InventoryWindow, HudWindow
from util.cursor import Cursor
import functools
from combat.attacks.ranged.base import RangedAttack
from combat import AttackContext
import math


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
            12, 110, layout_options=LayoutOptions(top=None, height=12, bottom=0, left=1, right=None, width=0.98))
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
        self.cursor = None

    def terminal_read(self, val):
        # TODO It would be nice to only set moved=True if the action succeeded.
        player = self.game_context.player
        moved = False

        if self.cursor:
            if val in self.movement_keys:
                key_x, key_y = self.movement_keys[val]
                actions.move(self.cursor, key_x, key_y)
                return

            if val == terminal.TK_ENTER:
                self.cursor.on_enter()
                self.cursor = None
                self.game_view.camera.character_focus = player

            if val == terminal.TK_ESCAPE:
                self.cursor = None
                self.game_view.camera.character_focus = player

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

        if val is terminal.TK_F:
            closest_monster = self.get_closest_monster(player)
            ranged_weapon = RangedAttack.get_ranged_weapon(player)
            EchoService.singleton.echo("You are aiming with " + ranged_weapon.name)

            def attack_wrapper(_monster):
                attack_context = AttackContext(
                    attacker=player,
                    defender=_monster,
                    attacker_weapon=ranged_weapon,
                    ranged=True
                )
                if _monster.location.get_local_coords() in player.fov:
                    actions.attack(player, _monster, attack_context)
                    self.update_turn(player)

            if closest_monster:
                self.cursor = Cursor(closest_monster.location.copy(), attack_wrapper)
            else:
                self.cursor = Cursor(player.location.copy(), attack_wrapper)
            self.game_view.camera.character_focus = self.cursor

        if val is terminal.TK_X:
            def clear_cursor(monster):
                self.cursor = None
                self.game_view.camera.character_focus = player

            self.cursor = Cursor(player.location.copy(), clear_cursor)
            self.game_view.camera.character_focus = self.cursor
            return

        if moved:
            self.update_turn(player)

    def update_turn(self, player):
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
        generator = random.choice(
            (
                forest_generator.ForestGenerator,
                dungeon_generator.DungeonGenerator
            )
        )(self.game_context.factory_service)

        player = self.game_context.player
        player.is_player = True

        generator.generate(level)
        self.place_dungeon_objects(level, player, generator)

    def place_dungeon_objects(self, level, player, generator):
        character_factory = self.game_context.character_factory
        item_factory = self.game_context.item_factory
        level.monster_spawn_list = [character_factory.build(uid) for uid, monster in character_templates.items()]
        level.item_spawn_list = [item_factory.build(uid) for uid, item in item_templates.items()]

        forerunner = generator.forerunner(level, player)
        forerunner.run()

    def get_closest_monster(self, player):
        closest_delta = None
        closest_monster = None
        p_x, p_y = player.location.get_local_coords()
        for monster in player.location.level.spawned_monsters:
            if monster.is_dead():
                continue
            monster_x, monster_y = monster.location.get_local_coords()
            delta = abs(p_x - monster_x) + abs(p_y - monster_y)
            if closest_delta is None:
                closest_delta = delta
                closest_monster = monster
                continue

            if delta < closest_delta:
                closest_monster = monster
                closest_delta = delta

        if closest_monster.location.get_local_coords() in player.fov:
            return closest_monster
        return None
