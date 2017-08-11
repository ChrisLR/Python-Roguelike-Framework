from base.scene import BaseScene
from managers.console_manager import Menu
from ui.flavor_text import MAIN_MENU


class MainMenuScene(BaseScene):
    ID = "MainMenu"

    def __init__(self, console_manager, game_context):
        super().__init__(console_manager, game_context)
        self.menu = Menu(MAIN_MENU['name'],
                         MAIN_MENU['text'],
                         MAIN_MENU['options'],
                         self.main_console.width,
                         self.main_console.height)
        self.current_x = 20
        self.current_y = 20.
        self.menu.create_menu(self.current_x, self.current_y)

    def render(self, is_active):
        self.main_console.blit(self.menu, 0, 0)

    def handle_input(self, char, mouse_events):
        if char.upper() == 'A':
            self.transition_to("CharacterCreationScene")
        elif char.upper() == 'B':
            # Halt the script using SystemExit
            raise SystemExit('The window has been closed.')
