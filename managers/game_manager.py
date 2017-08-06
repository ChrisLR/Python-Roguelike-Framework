from cocos.director import director

from managers.game_context import GameContext
from factories.body_factory import BodyFactory
from factories.character_factory import CharacterFactory
from factories.factory_service import FactoryService
from factories.item_factory import ItemFactory
from scenes.main_menu.scene import MainMenuScene


class GameManager(object):
    """
    Game Manager: Handles setup and progression of the game
    Admittedly this is a bit of a mess and will need to be cleaned up.
    """
    def __init__(self):
        # Pre-load levels into database
        self.game_context = GameContext()
        director.init()
        # self.console_manager = ConsoleManager()
        # self.game_context.console_manager = self.console_manager
        self.load_game_data()

    def start(self):
        director.run(MainMenuScene(self.game_context, self.scene_manager))

    def load_game_data(self):
        """
        This is where the game templates / data is loaded.
        """
        self.game_context.factory_service = FactoryService(body_factory=BodyFactory())
        factory_service = self.game_context.factory_service
        character_factory = CharacterFactory(factory_service=self.game_context.factory_service)
        factory_service.character_factory = character_factory
        self.game_context.character_factory = character_factory
        self.game_context.body_factory = factory_service.body_factory
        self.game_context.item_factory = ItemFactory()
