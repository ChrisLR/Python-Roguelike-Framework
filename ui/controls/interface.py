class ControlsInterface(object):
    def __init__(self, parent):
        self.parent = parent
        self.controls = []
        self.active_control_index = 0

    def add_control(self, control, x, y):
        self.controls.append(control)
        control.position = x, y
        parent_x, parent_y = self.parent.position
        control.world_position = (parent_x + x, parent_y + y)

    def render(self, console, active):
        for index, control in enumerate(self.controls):
            if self.active_control_index == index:
                control.render(console, True)
            else:
                control.render(console, False)

    def handle_input(self, key_events, mouse_events):
        if not self.controls:
            return
        active_control = self.controls[self.active_control_index]
        active_control.handle_input(key_events, [])
        for mouse_event in mouse_events:
            if mouse_event.type == 'MOUSEDOWN':
                for index, control in enumerate(self.controls):
                    if control.world_intersect(mouse_event.cell, (1, 1)):
                        self.active_control_index = index
                        control.on_press_function()
                        return
