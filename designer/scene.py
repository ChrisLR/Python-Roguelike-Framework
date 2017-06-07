import tdl
from managers.console_manager import Menu
from ui import controls


class DesignScene(object):
    ID = "CharacterCreation"

    def __init__(self, main_console):
        super().__init__()
        self.main_console = main_console
        # TODO Add windows for rendering designs, another for selecting things to add
        # TODO We'll need a few buttons for Add/Select/Remove modes of clicking
        # TODO We'll also need a save/delete/reset button for design pieces.

    def render(self):
        # TODO Render window here
        self.main_console.blit(self.menu, 0, 0)
        tdl.flush()

    def handle_input(self, key_events):
        # TODO This should mostly pass input to the windows.
        pass
