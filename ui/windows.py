import tdl

from base.window import BaseWindow
from ui.controls.interface import ControlsInterface
from util.operations import intersect


class SingleWindow(BaseWindow):
    def __init__(self, main_console, x=0, y=0):
        self.main_console = main_console
        self.window = tdl.Window(
            self.main_console, x, y,
            width=self.main_console.width,
            height=self.main_console.height
        )
        self.controls = ControlsInterface(self)

    def render(self, active):
        self.window.move(0, 0)
        self.controls.render(self.window, active)

    def handle_input(self, key_events, mouse_events):
        self.controls.handle_input(key_events, mouse_events)

    @property
    def position(self):
        return self.window.x, self.window.y


class MultipartWindow(BaseWindow):
    def __init__(self, main_console, windows):
        self.main_console = main_console
        self.windows = windows
        self.active_window_index = 0

    def render(self, active):
        for index, window in enumerate(self.windows):
            if index == self.active_window_index:
                window.render(True)
            else:
                window.render(False)

    def handle_input(self, key_events, mouse_events=None):
        for key_event in key_events:
            if key_event.key == "TAB":
                self.active_window_index += 1
                if self.active_window_index >= len(self.windows):
                    self.active_window_index = 0

        active_window = self.windows[self.active_window_index]
        if active_window:
            active_window.handle_input(key_events, [])
        for mouse_event in mouse_events:
            if mouse_event.type == 'MOUSEDOWN':
                for index, window in enumerate(self.windows):
                    if intersect((window.window.x, window.window.y), (window.window.width, window.window.height), mouse_event.cell, (1, 1)):
                        self.active_window_index = index
                        window.handle_input([], mouse_events)

