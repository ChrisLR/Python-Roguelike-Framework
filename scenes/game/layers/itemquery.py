import math

import tdl
from ui import controls
from ui.windows import SingleWindow


class ItemQueryWindow(SingleWindow):
    def __init__(self, main_console, callback_function, wielded_items, worn_items, inventory_items):
        super().__init__(main_console, )
        self.main_console = main_console
        self.window = tdl.Window(
            self.main_console, 0, 0,
            width=int(math.floor(self.main_console.width)),
            height=self.main_console.height
        )
        self.wielded_items_control = controls.ListChoiceControl(
            "Wielded Items:", wielded_items, self.window
        )
        self.worn_items_control = controls.ListChoiceControl(
            "Worn Items:", worn_items, self.window
        )
        self.inventory_items_control = controls.ListChoiceControl(
            "Items:", inventory_items, self.window
        )
        self.callback_function = callback_function
        self.controls = [self.wielded_items_control, self.worn_items_control, self.inventory_items_control]

    def handle_input(self, key_events, mouse_events):
        super().handle_input(key_events, mouse_events)
        active_control = self.controls[self.active_control_index]
        if active_control:
            active_control.handle_input(key_events, mouse_events)
            if active_control.finished:
                self.callback_function(active_control.answer)
