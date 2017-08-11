import cocos
from components.component import Component


class CocosLabelComponent(Component, cocos.text.Label):
    """Base class for components"""
    NAME = "cocos"

    def __init__(self, *args, **kwargs):
        """
        THIS HERE SHOULD BE INSTANTIATED AND REGISTERED
        """
        Component.__init__(self)
        cocos.text.Label.__init__(self, *args, **kwargs)

    def update(self):
        # TODO This should keep the CocosNode updated for each player action.
        pass


class CocosSpriteComponent(Component, cocos.sprite.Sprite):
    """Base class for components"""
    NAME = "cocos"

    def __init__(self):
        super().__init__()

    def update(self):
        # TODO This should keep the CocosNode updated for each player action.
        pass

