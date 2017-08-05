from settings import ControlColors
from ui.controls.base import BaseControl
from ui.controls.interface import ControlsInterface


class DockableList(BaseControl):
    def __init__(self, text, child_controls, foreground_color, background_color):
        super().__init__()
        self._text = text
        self.controls = ControlsInterface(self)
        x, y = self.position
        for child_control in child_controls:
            y += 1
            self.controls.add_control(child_control, x, y)
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.expanded = False
        self.dimensions = (len(text), 1)

    @property
    def text(self):
        return self._text + "\n"
    
    def on_press_function(self):
        if self.expanded:
            self.expanded = False
            self.dimensions = (len(self._text), 1)
        else:
            self.expanded = True
            max_width = max((len(control.text) for control in self.controls.controls))
            self.dimensions = (max_width, 1 + len(self.controls.controls))

    def render(self, console, active):
        if active:
            color = ControlColors.ACTIVE_CONTROL_COLOR
        else:
            color = self.foreground_color

        console.setColors(fg=color, bg=self.background_color)
        console.printStr(self.text)
        if self.expanded:
            self.controls.render(console, active)

    def handle_input(self, key_events, mouse_events):
        for key_event in key_events:
            if key_event.key == "ENTER":
                self.on_press_function()
        self.controls.handle_input(key_events, mouse_events)


    # TODO We will need to create a seperate handle_mouse event for everything.