from settings import ControlColors
from ui.controls.base import BaseControl


class DockableList(BaseControl):
    def __init__(self, text, child_controls, foreground_color, background_color):
        super().__init__()
        self._text = text
        self.child_controls = child_controls
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.expanded = False
        self.active_control_index = 0

    @property
    def text(self):
        return self._text
    
    def on_press_function(self):
        if self.expanded:
            self.expanded = False
        else:
            self.expanded = True

    def render(self, console, active):
        if active:
            color = ControlColors.ACTIVE_CONTROL_COLOR
        else:
            color = self.foreground_color

        console.setColors(fg=color, bg=self.background_color)
        self.set_position_before_render(console)
        console.printStr(self.text)
        if self.expanded:
            for index, control in enumerate(self.child_controls):
                if index == self.active_control_index:
                    control.render(console, True)
                else:
                    control.render(console, False)
                console.printStr("\n")
        self.set_dimension_after_render(console)

    def handle_input(self, key_events, mouse_events):
        for key_event in key_events:
            if key_event.key == "ENTER":
                self.on_press_function()

        # TODO THIS CONTROL MUST KEEP INTERNAL LABEL POSITION TO PROPERLY HIDE/SHOW
        # TODO THEN DISPATCH CLICKS TO EACH INDIVIDUAL CHILD COMPONENT
        for mouse_event in mouse_events:
            if mouse_event.type == 'MOUSEDOWN':
                for index, control in enumerate(self.child_controls):
                    mouse_x, mouse_y = mouse_event.cell
                    if control.intersect((mouse_x, mouse_y), (1, 1)):
                        control.on_press_function()
                        self.active_control_index = index



