import cocos
from cocos.menu import key


class PointDistributionMenuItem(cocos.menu.MenuItem):
    def __init__(self, attribute, callback_func, point_distribution):
        self.attribute = attribute
        self.point_distribution = point_distribution
        super().__init__(self._get_label(), callback_func)

    def _get_label(self):
        return '{}:{}'.format(self.attribute.value.capitalize(), self.point_distribution.get_value(self.attribute))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.point_distribution.decrease_value(self.attribute)
        elif symbol == key.RIGHT:
            self.point_distribution.increase_value(self.attribute)

        if symbol in (key.LEFT, key.RIGHT, key.ENTER):
            self.item.text = self._get_label()
            self.item_selected.text = self._get_label()
            self.callback_func(self.attribute, self.point_distribution.get_value(self.attribute))
            return True
