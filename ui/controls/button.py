from settings import ControlColors
from ui.controls.base import BaseControl


class Button(BaseControl):
    def __init__(self, text, on_press_function, foreground_color, background_color):
        super().__init__()
        self._text = text
        self.on_press_function = on_press_function
        self.foreground_color = foreground_color
        self.background_color = background_color

    @property
    def text(self):
        return self._text

    def render(self, console, active):
        if active:
            color = ControlColors.ACTIVE_CONTROL_COLOR
        else:
            color = self.foreground_color

        console.setColors(fg=color, bg=self.background_color)
        self.set_position_before_render(console)
        console.printStr(self.text)
        self.set_dimension_after_render(console)

    def handle_input(self, key_events, mouse_events):
        for key_event in key_events:
            if key_event.key == "ENTER":
                self.on_press_function()



