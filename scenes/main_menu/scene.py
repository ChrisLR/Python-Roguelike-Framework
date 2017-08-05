import cocos

from scenes.main_menu.layer import MainMenuUILayer


class MainMenuScene(cocos.scene.Scene):
    ID = "MainMenu"

    def __init__(self, game_context):
        self.layer = MainMenuUILayer()
        super().__init__(self.layer)
