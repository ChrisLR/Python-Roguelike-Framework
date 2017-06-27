"""
This is the scene module. 
"""
import abc


class BaseScene(object):
    """Abstract class for all scenes"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, console_manager, scene_manager, game_context):
        self.console_manager = console_manager
        self.main_console = console_manager.main_console
        self.scene_manager = scene_manager
        self.game_context = game_context
        self.active_windows = []

    def render(self):
        if self.active_windows:
            self.active_windows[0].render(True)

    def handle_input(self, key_events, mouse_events):
        for key_event in key_events:
            if key_event.keychar == "ESCAPE":
                self.close_window()

        if self.active_windows:
            self.active_windows[0].handle_input(key_events, mouse_events)

    def invoke_window(self, window):
        self.active_windows.insert(0, window)

    def close_window(self):
        if len(self.active_windows) > 1:
            self.active_windows.pop(0)
            return

    def transition_to(self, scene_name):
        self.scene_manager.transition_to(scene_name)
