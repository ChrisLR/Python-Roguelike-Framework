from .component import Component


class Display(Component):
    NAME = "display"

    def __init__(self, foreground_color, background_color, ascii_character):
        super().__init__()
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.ascii_character = ascii_character

    def get_draw_info(self):
        return "[hue={}]{}".format(self.foreground_color, self.ascii_character)

    def copy(self):
        new_instance = Display(self.foreground_color, self.background_color, self.ascii_character)
        return new_instance
