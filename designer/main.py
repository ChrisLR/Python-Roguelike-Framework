import tdl
import os
from designer.scene import DesignScene


# This Designer will need a multiscreen window.
# It will import all the python data and allow us to place things.
# We need to be able to place Items, Characters, Furnitures, Tiles
# Each new Design piece needs to have a X, Y Size set.
# Design pieces will be fitted with an identical tile.
# Meaning a Design piece with 6 x 6 Forest is compatible with itself and anything with a forest edge.
# Design pieces should be viewable/savable using this and filterable with a Theme Id
# When Generating we will have to convert design coords to local map coords.
class DesignerManager(object):
    def __init__(self, width=100, height=60):
        self.console = self.initialize_console(width, height)
        self.scene = DesignScene(self.console)

    @staticmethod
    def initialize_console(width, height):
        font_path = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "terminal8x8_gs_ro.png"))
        tdl.setFont(font_path)

        return tdl.init(width, height, 'Designer')

    def start(self):
        tdl.setTitle("Designer")
        while True:  # Continue in an infinite game loop.
            self.console.clear()
            self.scene.render()
            all_key_events = list(tdl.event.get())
            for key_event in all_key_events:
                if key_event.type == 'QUIT':
                    # Halt the script using SystemExit
                    raise SystemExit('The window has been closed.')
            key_events = [key_event for key_event in all_key_events if key_event.type == 'KEYDOWN']
            # TODO Do we want to handle mouse events too?
            # mouse_events = [key_event for key_event in all_key_events if key_event.type == 'MOUSEDOWN']

            self.scene.handle_input(key_events=key_events)
            tdl.flush()
