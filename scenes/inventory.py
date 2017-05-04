import math
import logging

import tdl

from base.scene import BaseScene
from managers.console_manager import Menu
from ui import controls


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class InventoryScene(BaseScene):
    ID = "Inventory"

    def __init__(self, console_manager, scene_manager, game_context):
        super().__init__(console_manager, scene_manager, game_context)
        self.item_list_window = ItemListWindow(self.main_console)
        self.item_detail_window = ItemDetailWindow(self.main_console)
        self.active_window = 0
        self.windows = [
            self.item_list_window,
            self.item_detail_window
        ]
        self.item_list_window.build(self.game_context.player)

    def render(self):
        for window in self.windows:
            window.render()

    def handle_input(self, key_events):
        for key_event in key_events:
            if key_event.key == "ESCAPE":
                self.transition_to("GameScene")
                return
            for window in self.windows:
                window.handle_input(key_events)

            if self.active_window == self.windows.index(self.item_list_window):
                if self.item_list_window.chosen_item is not None:
                    self.item_detail_window.build(self.item_list_window.chosen_item)
                    self.active_window = self.windows.index(self.item_detail_window)


class ItemListWindow(object):
    def __init__(self, main_console):
        self.main_console = main_console
        self.window = tdl.Window(
            self.main_console, 0, 0,
            width=int(math.floor(self.main_console.width / 2)),
            height=self.main_console.height
        )
        self.wielded_items_control = None
        self.worn_items_control = None
        self.inventory_items_control = None
        self.chosen_item = None

    def build(self, player):
        # TODO Not sure how often this should be rebuilt but at least every time the menu is opened
        # TODO and another every removed item
        if player and player.equipment:
            self.wielded_items_control = controls.ListChoiceControl(
                "Wielded Items:",
                player.equipment.get_wielded_items(),
                self.window
            )
            self.worn_items_control = controls.ListChoiceControl(
                "Worn Items:",
                player.equipment.get_worn_items(),
                self.window
            )
        if player and player.inventory:
            self.inventory_items_control = controls.ListChoiceControl(
                "Items:",
                player.inventory.get_all_items(),
                self.window
            )

    def render(self):
        self.window.move(0, 0)
        if self.wielded_items_control:
            self.wielded_items_control.render(self.window, True)
        if self.worn_items_control:
            self.worn_items_control.render(self.window, True)
        if self.inventory_items_control:
            self.inventory_items_control.render(self.window, True)

    def handle_input(self, key_events):
        # TODO Find an intuitive way to handle all three sections
        if self.inventory_items_control:
            self.inventory_items_control.handle_input(key_events)
            if self.inventory_items_control.finished:
                self.chosen_item = self.inventory_items_control.answer


class ItemDetailWindow(object):
    def __init__(self, main_console):
        self.main_console = main_console
        self.window = tdl.Window(
            self.main_console, int(math.floor(self.main_console.width / 2)) + 1, 0,
            width=int(math.floor(self.main_console.width / 2)),
            height=self.main_console.height
        )
        self.control = None
        self.chosen_item = None

    def build(self, item):
        # TODO This should be rebuilt every detailed item
        if item:
            # TODO Show Item Detail View here
            pass

    def render(self):
        self.window.move(0, 0)
        if self.control:
            self.control.render()

    def handle_input(self, key_events):
        if self.control:
            self.control.handle_input(key_events)
