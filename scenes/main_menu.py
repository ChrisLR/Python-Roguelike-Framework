from managers.console_manager import Menu
import tdl


class MainMenuScene(object):
    ID = "MainMenu"

    def __init__(self, console_manager, start_game_callback):
        self.console_manager = console_manager
        self.main_console = console_manager.main_console
        self.options = ['Play a new game', 'Quit']
        self.menu = Menu('Main Menu', self.options, self.main_console.width, self.main_console.height)
        self.current_x = 20
        self.current_y = 20
        self.start_game_callback = start_game_callback

    def get_next_y(self):
        self.current_y += 2
        return self.current_y

    def get_next_x(self):
        self.current_x += 5
        return self.current_x

    def render(self):
        x = self.current_x
        self.menu.print_str('Welcome', x, self.get_next_y())
        self.menu.print_str('Your goal is to find the Cone of Dunshire (!).', x, self.get_next_y())
        self.menu.print_str('Use Caution as there are Trolls (T) and Orcs (o)', x, self.get_next_y())
        self.menu.print_str('lurking in this areas!', x, self.get_next_y())

        x = self.get_next_x()
        for option_text in self.options:
            text = '(' + chr(self.menu.letter_index) + ') ' + option_text
            self.menu.print_str(text, x, self.get_next_y())
            self.menu.letter_index += 1
        self.main_console.blit(self.menu, 0, 0)
        tdl.flush()

    def handle_input(self):
        key_event = tdl.event.keyWait()
        if key_event.keychar.upper() == 'A':
            self.start_game_callback()
        elif key_event.keychar.upper() == 'B':
            # Halt the script using SystemExit
            raise SystemExit('The window has been closed.')
