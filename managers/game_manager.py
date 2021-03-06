from clubsandwich.director import DirectorLoop
from bearlibterminal import terminal
from scenes.main_menu.scene import MainMenuScene

from managers.game_context import GameContext
from factories.character_factory import CharacterFactory
from factories.factory_service import FactoryService
from factories.item_factory import ItemFactory


class GameManager(object):
    """
    Game Manager: Handles setup and progression of the game
    Admittedly this is a bit of a mess and will need to be cleaned up.
    """
    def __init__(self):

        # Pre-load levels into database
        self.game_context = GameContext()
        self.load_game_data()

    def start(self):
        loop = MainLoop(MainMenuScene(self.game_context))
        loop.run()
        # while True:  # Continue in an infinite game loop.
        #     self.console_manager.main_console.clear()  # Blank the console
        #     self.scene_manager.render_current_scene()
        #     all_key_events = list(tdl.event.get())
        #     for key_event in all_key_events:
        #         if key_event.type == 'QUIT':
        #             # Halt the script using SystemExit
        #             raise SystemExit('The window has been closed.')
        #     key_events = [key_event for key_event in all_key_events if key_event.type == 'KEYDOWN']
        #     mouse_events = [key_event for key_event in all_key_events if key_event.type in ['MOUSEDOWN', 'MOUSEUP']]
        #
        #     self.scene_manager.handle_input(key_events=key_events, mouse_events=mouse_events)
        #     tdl.flush()

    def load_game_data(self):
        """
        This is where the game templates / data is loaded.
        """
        self.game_context.factory_service = FactoryService()
        factory_service = self.game_context.factory_service
        character_factory = CharacterFactory(factory_service=self.game_context.factory_service)
        factory_service.character_factory = character_factory
        self.game_context.character_factory = character_factory
        self.game_context.item_factory = ItemFactory()


class MainLoop(DirectorLoop):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene

    def get_initial_scene(self):
        return self.scene

    def terminal_init(self):
        super().terminal_init()
        terminal.set("window: title='Python Roguelike Template', size=120x50;")
