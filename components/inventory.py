from components.component import Component


class Inventory(Component):
    NAME = "inventory"
    """
    The inventory object containing Items via ItemSlots.
    While getting an item from an item seems useless it's to be combined with another type of inventory.
    See Keybound below which is meant for a player.
    """
    def __init__(self):
        super().__init__()
        self._items = []
        self._destroyed_items = []

    def clear_destroyed_items(self):
        for item in self._destroyed_items:
            self._items.remove(item)
        self._destroyed_items = []

    def copy(self):
        new_copy = Inventory()
        for item in self._items:
            new_copy._items.append(item.copy())

        return new_copy

    def add_item(self, item):
        self._items.append(item)

    def remove_item(self, item):
        self._items.remove(item)

    def get_items(self, uid, count=0, pop=False):
        """
        :param uid: uid of item to get.
        :param count: How many to retrieve.
        :param pop: bool to know if we remove it or not.
        :return: List of items found.
        """
        found_items = []
        for item in self._items:
            if item.destroyed:
                self._destroyed_items.append(item)
                continue

            if count and len(found_items) >= count:
                break
            if item.uid == uid:
                found_items.append(item)
                if pop:
                    self.remove_item(item)

        self.clear_destroyed_items()
        return found_items

    def get_all_items(self):
        for item in self._items:
            if item.destroyed:
                self._destroyed_items.append(item)
        self.clear_destroyed_items()

        return self._items


class KeyBoundInventory(Inventory):
    # noinspection SpellCheckingInspection
    CHARACTER_SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789°!\"#$%?&*()_+^:'.|{}[]@"
    """
    This inventory keeps ascii bindings to added items.
    Used for the player.
    """
    def __init__(self):
        super(KeyBoundInventory, self).__init__()
        self._page = 0
        self._max_page = 0
        self._unassigned_symbols = {0: list(KeyBoundInventory.CHARACTER_SET)}
        self._assigned_symbols = {0: {}}

    def add_item(self, item):
        if item not in self._items:
            super(KeyBoundInventory, self).add_item(item)
            next_symbol = self.__return_next_assigned_symbol()
            self._assigned_symbols[self._page][next_symbol] = item
            return next_symbol

        super(KeyBoundInventory, self).add_item(item)
        return self.get_symbol_from_item(item)

    def clear_destroyed_items(self):
        for item in self._destroyed_items:
            self.pop_item_from_symbol(self.get_symbol_from_item(item))
        self._destroyed_items = []

    def get_symbol_from_uid(self, item_uid):
        return next(
            (symbol for page, symbols in self._assigned_symbols.items()
             for symbol, item in symbols.items() if item.uid == item_uid))

    def get_symbol_from_item(self, item):
        for page in self._assigned_symbols.keys():
            for key, value in self._assigned_symbols[page].items():
                if value == item:
                    return key

    def pop_item_from_symbol(self, symbol):
        self._unassigned_symbols[self._page].append(symbol)
        item = self._assigned_symbols[self._page].pop(symbol)
        self.remove_item(item)
        return item

    def get_assigned_symbols(self, page):
        return {symbol: name for symbol, name in self._assigned_symbols[page].items()}

    def __return_next_assigned_symbol(self):
        if not self._unassigned_symbols[self._page]:
            page = self.__find_available_page_or_create()
            return self._unassigned_symbols[page].pop(0)
        return self._unassigned_symbols[self._page].pop(0)

    def __find_available_page_or_create(self):
        for page, available_symbols in self._unassigned_symbols.items():
            if available_symbols:
                return page
        self._max_page += 1
        self._unassigned_symbols[self._max_page] = list(self.CHARACTER_SET)
        return self._max_page
