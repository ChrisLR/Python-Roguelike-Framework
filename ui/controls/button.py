from settings import ControlColors
from ui.controls.base import BaseControl


class Button(BaseControl):
    def __init__(self, text, on_press_function, foreground_color, background_color):
        super().__init__()
        self._text = text
        self.on_press_function = on_press_function
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.dimensions = (len(text), 1)

    @property
    def text(self):
        return self._text

    def render(self, console, active):
        if active:
            color = ControlColors.ACTIVE_CONTROL_COLOR
        else:
            color = self.foreground_color

        x, y = self.position
        console.drawStr(x, y, self.text, color, self.background_color)

    def handle_input(self, key_events, mouse_events):
        for key_event in key_events:
            if key_event.key == "ENTER":
                self.on_press_function()



