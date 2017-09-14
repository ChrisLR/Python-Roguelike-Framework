from components.game_object import GameObject
import stats


class Item(GameObject):
    NAME = "item"
    """
    What is an item?
    It made out of a material, it has a type, it can be used.
    It has stats, it can be destroyed, displayed, held.
    It can have a rarity, a level, value.
    It can be sharpened, altered, destroyed and repaired.
    Painted, customized, engraved.
    A good loot system can go a long way in terms of extending play time.
    """
    def __init__(self, uid, name="", description="", location=None, display=None, size=None, weight=None):
        super().__init__()
        self.uid = uid
        self._name = name
        self._description = description
        if location:
            self.register_component(location)
        if display:
            self.register_component(display)
        self.size = stats.Stat(size.value)
        self.weight = weight

    @property
    def description(self):
        """
        This property will be able to return altered descriptions for customized items.
        :return: String of current description.
        """
        return self._description

    @property
    def name(self):
        """
        This property will be able to return engraved names for customized items.
        :return: String of current name.
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def copy(self):
        new_item = Item(self.uid, self._name, self._description, self.display, size=self.size)
        return super().copy_to(new_item)

