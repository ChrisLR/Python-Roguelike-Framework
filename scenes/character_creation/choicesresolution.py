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
            ButtonView(choice.name if hasattr(choice, 'name') else str(choice),
                       callback=partial(self.callback_and_pop_scene, callback, choice, choice_name))
            for choice in choices
        ]

        window_view = WindowView(
            choice_name,
            subviews=[
                KeyAssignedListView(
                    choices,
                    value_column_width=16,
                ),
            ],
            layout_options=LayoutOptions(left=0.25, width=0.3, height=0.5, top=0.25, right=None, bottom=None)
        )
        super().__init__(window_view)

    @staticmethod
    def callback_and_pop_scene(callback, choice, choice_name):
        callback(choice, choice_name)

    def terminal_read(self, val):
        super().terminal_read(val)
        if val == terminal.TK_ESCAPE:
            self.director.pop_scene()
