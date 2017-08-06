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

        # TODO Add layers for rendering designs, another for selecting things to add
        # TODO We'll need a few buttons for Add/Select/Remove modes of clicking
        # TODO We'll also need a save/delete/reset button for design pieces.

    def new_design_piece(self):
        self.design_piece = DesignPiece.empty(6, 6)

    def save_design_piece(self):
        pass

    def load_design_piece(self):
        pass

    def select_tile(self, tile):
        pass

    def render(self):
        self.main_window.render(True)
        tdl.flush()

    def handle_input(self, key_events, mouse_events):
        self.main_window.handle_input(key_events, mouse_events)

