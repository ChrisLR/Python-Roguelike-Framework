from functools import partial

from bearlibterminal import terminal
from clubsandwich.ui import (
    UIScene,
    WindowView,
    LayoutOptions,
    KeyAssignedListView,
    ButtonView
)


class ChoicesResolutionWindow(UIScene):
    def __init__(self, callback, choice_name, choices):
        choices = [
            ButtonView(str(choice), callback=partial(self.callback_and_pop_scene, callback, choice, choice_name))
            for choice in choices
        ]

        window_view = WindowView(
            choice_name,
            subviews=[
                KeyAssignedListView(
                    choices,
                    value_column_width=16,
                    layout_options=LayoutOptions(left=0.1, width=0.3, height=0.3, top=0, right=None, bottom=None)
                ),
            ]
        )
        super().__init__(window_view)
        self.covers_screen = False

    @staticmethod
    def callback_and_pop_scene(callback, choice, choice_name):
        callback(choice, choice_name)

    def terminal_read(self, val):
        super().terminal_read(val)
        if val == terminal.TK_ESCAPE:
            self.director.pop_scene()
