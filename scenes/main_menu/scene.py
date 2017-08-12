from clubsandwich.ui.misc_views import LabelView, ButtonView
from clubsandwich.ui.ui_scene import UIScene
from clubsandwich.ui import LayoutOptions

from scenes.character_creation.scene import CharacterCreationScene
from ui.flavor_text import MAIN_MENU


class MainMenuScene(UIScene):
    ID = "MainMenu"

    def __init__(self, game_context):
        views = [
            LabelView(
                text=MAIN_MENU["name"],
                align_vert='top',
                layout_options=LayoutOptions.row_top(5),
            ),
            LabelView(
                text=MAIN_MENU["text"],
                layout_options=LayoutOptions.row_top(10)
            ),
            ButtonView(
                text="Play",
                callback=lambda: self.director.replace_scene(CharacterCreationScene(game_context)),
                layout_options=LayoutOptions.row_bottom(0.5).with_updates(
                    left=0, width=0.5, right=None)
            ),
            ButtonView(
                text="Quit",
                callback=lambda: self.director.quit(),
                layout_options=LayoutOptions.row_bottom(0.5).with_updates(
                    left=0.2, width=0.5, right=None),
            )
        ]
        super().__init__(views)

