from ui.controls import Button, DockableList
from ui.windows import MultipartWindow, SingleWindow
from data.python_templates.tiles import tiles
from data.python_templates.items import item_templates
from data.python_templates.characters import character_templates
from util.colors import Colors


class WindowDesignerMain(MultipartWindow):
    def __init__(self, main_console, scene):
        windows = [
            WindowHeaderButtons(main_console, scene),
            WindowRenderDesign(main_console, scene, 0, 1),
            WindowSelectCreation(main_console, scene, 20, 0)
        ]
        super().__init__(main_console, windows)


class WindowRenderDesign(SingleWindow):
    def __init__(self, main_console, scene, x=0, y=0):
        super().__init__(main_console, x, y)
        self.scene = scene

    def render(self, active):
        self.window.move(0, 0)
        design_piece = self.scene.design_piece

        for x in range(0, self.scene.design_piece.size_x):
            for y in range(0, self.scene.design_piece.size_y):
                # Render
                tile = next((tile for tile in tiles if tile.uid == design_piece.tile_ids[x][y]), None)
                item = item_templates.get(design_piece.item_ids[x][y], None)
                character = character_templates.get(design_piece.character_ids[x][y], None)
                if tile:
                    self.window.drawChar(x, y, **tile.display.get_draw_info())
                if item:
                    self.window.drawChar(x, y, **item.display.get_draw_info())
                if character:
                    self.window.drawChar(x, y, **character.display.get_draw_info())
                # TODO Eventually furniture_ids


class WindowHeaderButtons(SingleWindow):
    def __init__(self, main_console, scene, x=0, y=0):
        super().__init__(main_console, x, y)
        self.scene = scene
        self.controls.add_control(Button(" New ", self.scene.new_design_piece, Colors.BLACK, Colors.GRAY), x, y)
        self.controls.add_control(Button(" Save ", self.scene.save_design_piece, Colors.BLACK, Colors.GRAY), x + 4, y)
        self.controls.add_control(Button(" Load ", self.scene.load_design_piece, Colors.BLACK, Colors.GRAY), x + 9, y)


class WindowSelectCreation(SingleWindow):
    def __init__(self, main_console, scene, x=0, y=0):
        super().__init__(main_console, x, y)
        self.scene = scene
        self.controls.add_control(
            DockableList("Tiles",
                         [Button(tile.uid,
                                 lambda: self.scene.select_tile(tile),Colors.BLACK, Colors.GRAY) for tile in tiles],
                         Colors.BLACK, Colors.GRAY), 0, 0)


