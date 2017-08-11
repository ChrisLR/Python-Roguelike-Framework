import cocos


class HUDLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        width = cocos.director.director.window.width
        height = cocos.director.director.window.height / 3
        self.console = cocos.text.Label(x=0, y=height, width=width, height=height, multiline=True, text="")
        self.add(self.console)
