from clubsandwich.ui import UIScene, WindowView, LayoutOptions, KeyAssignedListView, ButtonView, Scene


class InventoryWindow(UIScene):
    def __init__(self, wielded_items, worn_items, inventory_items):
        wielded_button_generator = (
            ButtonView(item.name, lambda: self.describe_item(item))
            for item in wielded_items
        )
        worn_button_generator = (
            ButtonView(item.name, lambda: self.describe_item(item))
            for item in worn_items
        )
        inventory_button_generator = (
            ButtonView(item.name, lambda: self.describe_item(item))
            for item in inventory_items
        )
        wielded_view = WindowView(
            'Wielded Items',
            layout_options=LayoutOptions.centered(60, 20),
            subviews=[KeyAssignedListView(wielded_button_generator)]
        )
        worn_view = WindowView(
            'Worn Items',
            layout_options=LayoutOptions.centered(60, 20),
            subviews=[KeyAssignedListView(worn_button_generator)]
        )
        inventory_view = WindowView(
            'Inventory',
            layout_options=LayoutOptions.centered(60, 20),
            subviews=[KeyAssignedListView(inventory_button_generator)]
        )
        super().__init__([wielded_view, worn_view, inventory_view])

    def describe_item(self, item):
        self.director.push_scene(ItemDetailWindow(item))


class ItemDetailWindow(WindowView):
    def __init__(self, chosen_item):
        self.covers_screen = False
        view = WindowView(
            chosen_item.name
        )
        super().__init__()

    def terminal_read(self, val):
        self.director.pop_scene()


