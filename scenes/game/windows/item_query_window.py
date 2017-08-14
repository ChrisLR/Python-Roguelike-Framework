from functools import partial

from bearlibterminal import terminal
from clubsandwich.ui import (
    UIScene,
    WindowView,
    LayoutOptions,
    KeyAssignedListView,
    ButtonView
)


class ItemQueryWindow(UIScene):
    def __init__(self, callback, wielded_items, worn_items, inventory_items):
        self.covers_screen = True
        wielded_buttons = [
            ButtonView(item.name, callback=partial(self.callback_and_pop_scene, callback, item))
            for item in wielded_items
        ]
        worn_buttons = [
            ButtonView(item.name, callback=partial(self.callback_and_pop_scene, callback, item))
            for item in worn_items
        ]
        inventory_buttons = [
            ButtonView(item.name, callback=partial(self.callback_and_pop_scene, callback, item))
            for item in inventory_items
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

    def callback_and_pop_scene(self, callback, item):
        callback(item)
        self.director.pop_scene()

    def terminal_read(self, val):
        super().terminal_read(val)
        if val == terminal.TK_ESCAPE:
            self.director.pop_scene()
