import math

import tdl
from ui import controls
from ui.windows import SingleWindow, MultipartWindow
from scenes.game.windows.item_query_window import ItemQueryWindow


class InventoryWindow(MultipartWindow):
    def __init__(self, main_console, wielded_items, worn_items, inventory_items):
        self.item_query_window = ItemQueryWindow(
            main_console, self.build_item_detail_window,
            wielded_items, worn_items, inventory_items
        )
        super().__init__(main_console, [self.item_query_window])

    def build_item_detail_window(self, chosen_item):
        self.windows = [self.item_query_window, ItemDetailWindow(self.main_console, chosen_item)]


class ItemDetailWindow(SingleWindow):
    def __init__(self, main_console, chosen_item):
        super().__init__(main_console)
        self.window = tdl.Window(
            self.main_console, int(math.floor(self.main_console.width / 2)) + 1, 0,
            width=int(math.floor(self.main_console.width / 2)),
            height=self.main_console.height
        )
        # TODO This window should show details on whatever Item was selected.
        self.control = None
        self.chosen_item = chosen_item

