from functools import partial

from bearlibterminal import terminal
from clubsandwich.ui import (
    UIScene,
    WindowView,
    LayoutOptions,
    KeyAssignedListView,
    ButtonView,
    LabelView
)


class InventoryWindow(UIScene):
    def __init__(self, wielded_items, worn_items, inventory_items):
        self.covers_screen = True
        wielded_buttons = [
            ButtonView(item.name, callback=partial(self.describe_item, item))
            for item in sorted(set(wielded_items), key=lambda item: item.name)
        ]
        worn_buttons = [
            ButtonView(item.name, callback=partial(self.describe_item, item))
            for item in sorted(set(worn_items), key=lambda item: item.name)
        ]
        inventory_buttons = [
            ButtonView(item.name, callback=partial(self.describe_item, item))
            for item in sorted(set(inventory_items), key=lambda item: item.name)
        ]

        window_view = WindowView(
            "Items",
            subviews=[
                KeyAssignedListView(
                    wielded_buttons,
                    value_column_width=16,
                    layout_options=LayoutOptions(left=0.1, width=0.3, height=0.3, top=0, right=None, bottom=None)
                ),
                KeyAssignedListView(
                        worn_buttons,
                        value_column_width=16,
                        layout_options=LayoutOptions(left=0.1, width=0.3, height=0.3, top=0.3, right=None, bottom=None)
                ),
                KeyAssignedListView(
                        inventory_buttons,
                        value_column_width=16,
                        layout_options=LayoutOptions(left=0.1, width=0.3, height=0.3, top=0.6, right=None, bottom=None)
                )
            ]
        )
        super().__init__(window_view)

    def describe_item(self, item):
        self.director.push_scene(ItemDetailWindow(item))

    def terminal_read(self, val):
        super().terminal_read(val)
        if val == terminal.TK_ESCAPE:
            self.director.pop_scene()


class ItemDetailWindow(UIScene):
    def __init__(self, chosen_item):
        self.covers_screen = False
        view = WindowView(
            chosen_item.name,
            layout_options=LayoutOptions(left=None, width=0.3, height=0.7, top=0.05, right=0.25, bottom=None),
            subviews=[
                LabelView(chosen_item.description)
            ]
        )
        super().__init__(view)

    def terminal_read(self, val):
        self.director.pop_scene()
