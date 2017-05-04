import math
import tdl

from base.window import BaseWindow


class SingleWindow(BaseWindow):
    def __init__(self, main_console):
        self.main_console = main_console
        self.window = tdl.Window(
            self.main_console, 0, 0,
            width=self.main_console.width,
            height=self.main_console.height
        )
        self.controls = []
        self.active_control_index = 0

    def render(self):
        self.window.move(0, 0)
        for index, control in enumerate(self.controls):
            if index == self.active_control_index:
                control.render(console=self.window, active=True)
            else:
                control.render(console=self.window, active=False)

    def handle_input(self, key_events):
        for key_event in key_events:
            if key_event.key == "TAB":
                self.active_control_index += 1
                if self.active_control_index >= len(self.controls) + 1:
                    self.active_control_index = 0

        if self.controls:
            active_control = self.controls[self.active_control_index]
            if active_control:
                active_control.handle_input(key_events)


class MultipartWindow(BaseWindow):
    def __init__(self, main_console, windows):
        self.main_console = main_console
        self.windows = windows
        self.active_window_index = 0

    def render(self):
        for window in self.windows:
            window.render()

    def handle_input(self, key_events):
        for key_event in key_events:
            if key_event.key == "TAB":
                self.active_window_index += 1
                if self.active_window_index >= len(self.windows):
                    self.active_window_index = 0

        active_window = self.windows[self.active_window_index]
        if active_window:
            active_window.handle_input(key_events)
