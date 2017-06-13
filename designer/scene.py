import tdl
from designer.windows import WindowDesignerMain
from designer.design import DesignPiece


class DesignScene(object):
    ID = "CharacterCreation"

    def __init__(self, main_console):
        super().__init__()
        self.design_piece = DesignPiece.empty(6, 6)
        self.main_console = main_console
        self.main_window = WindowDesignerMain(main_console, self)

        # TODO Add windows for rendering designs, another for selecting things to add
        # TODO We'll need a few buttons for Add/Select/Remove modes of clicking
        # TODO We'll also need a save/delete/reset button for design pieces.

    def render(self):
        self.main_window.render()
        tdl.flush()

    def handle_input(self, key_events):
        # TODO This should mostly pass input to the windows.
        pass
