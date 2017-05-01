import math
import logging

import tdl

from base.scene import BaseScene
from managers.console_manager import Menu
from ui import controls


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class InventoryQueryScene(BaseScene):
    ID = "InventoryQuery"

    def __init__(self, console_manager, scene_manager, game_context, **kwargs):
        super().__init__(console_manager, scene_manager, game_context)
        self.item_query_window = ItemQueryWindow(self.main_console)
        self.active_window = 0
        self.windows = [
            self.item_query_window,
        ]
        self.callback_function = None
        self.on_switch(**kwargs)


    def on_switch(self, **kwargs):
        if "player" not in kwargs:
            logger.error("InventoryQueryScene: Player was not given in kwargs.")
            return

        if 'callback_function' not in kwargs:
            logger.error("InventoryQueryScene: Callback Function was not given in kwargs.")
        self.callback_function = kwargs['callback_function']

        player = kwargs["player"]
        self.item_query_window.build(player)

    def render(self, **kwargs):
        for window in self.windows:
            window.render(**kwargs)

    def handle_input(self, **kwargs):
        key_events = kwargs["key_events"]
        for key_event in key_events:
            if key_event.key == "ESCAPE":
                self.transition_to("GameScene")
                return
            for window in self.windows:
                window.handle_input(**kwargs)

        if self.item_query_window.chosen_item:
            self.transition_to('GameScene')
            self.callback_function(chosen_item=self.item_query_window.chosen_item)


class ItemQueryWindow(object):
    def __init__(self, main_console):
        self.main_console = main_console
        self.window = tdl.Window(
            self.main_console, 0, 0,
            width=int(math.floor(self.main_console.width)),
            height=self.main_console.height
        )
        self.wielded_items_control = None
        self.worn_items_control = None
        self.inventory_items_control = None
        self.chosen_item = None
        self.active_section_index = 0
        self.sections = []

    def build(self, player):
        # TODO Not sure how often this should be rebuilt.
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

        self.active_section_index = 0
        self.sections = [self.wielded_items_control, self.worn_items_control, self.inventory_items_control]

    def render(self, **kwargs):
        self.window.move(0, 0)
        active_control = self.sections[self.active_section_index]
        for control in self.sections:
            if control == active_control:
                control.render(self.window, True, **kwargs)
            else:
                control.render(self.window, False, **kwargs)

    def handle_input(self, **kwargs):
        key_events = kwargs["key_events"]
        for key_event in key_events:
            if key_event.key == "TAB":
                self.active_section_index += 1
                if self.active_section_index >= len(self.sections):
                    self.active_section_index = 0

        active_control = self.sections[self.active_section_index]
        if active_control:
            active_control.handle_input(**kwargs)
            if active_control.finished:
                self.chosen_item = active_control.answer
