from clubsandwich.ui.misc_views import LabelView, ButtonView
from clubsandwich.ui.ui_scene import UIScene
from clubsandwich.ui import LayoutOptions

from scenes.character_creation.scene import CharacterCreationScene
from ui.flavor_text import MAIN_MENU


class MainMenuScene(UIScene):
    ID = "MainMenu"

    def __init__(self, game_context):
        self.covers_screen = True
        views = [
            LabelView(
                text=MAIN_MENU["text"],
                layout_options=LayoutOptions(top=0.4, height=0.1, bottom=None)
            ),
            ButtonView(
                text="Play",
                callback=lambda: self.director.replace_scene(CharacterCreationScene(game_context)),
                layout_options=LayoutOptions(top=0.5, height=0.2, left=0.4, right=None, bottom=None, width=0.1),
            ),
            ButtonView(
                text="Quit",
                callback=lambda: self.director.quit(),
                layout_options=LayoutOptions(top=0.5, height=0.2, left=0.5, right=None, bottom=None, width=0.1)
            )
        ]
        super().__init__(views)

