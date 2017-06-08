from ui.windows import MultipartWindow, SingleWindow


class WindowDesignerMain(MultipartWindow):
    def __init__(self, main_console, scene):
        windows = [
            WindowHeaderButtons(main_console, scene),
            WindowRenderDesign(main_console, scene),
            WindowSelectCreation(main_console, scene)
        ]
        super().__init__(main_console, windows)


class WindowRenderDesign(SingleWindow):
    def __init__(self, main_console, scene):
        super().__init__(main_console)
        self.scene = scene

    def render(self):
        self.window.move(0, 0)

        for x in range(0, self.scene.design_piece.size_x):
            for xy in range(0, self.scene.design_piece.size_y):
                # Render
                # tile_ids
                # item_ids
                # character_ids
                # Eventually furniture_ids

                pass


class WindowHeaderButtons(SingleWindow):
    def __init__(self, main_console, scene):
        super().__init__(main_console)
        self.scene = scene


class WindowSelectCreation(SingleWindow):
    def __init__(self, main_console, scene):
        super().__init__(main_console)
        self.scene = scene
