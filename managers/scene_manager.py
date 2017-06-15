from scenes import (
    CharacterCreationScene,
    GameScene,
    MainMenuScene
)


class SceneManager(object):
    def __init__(self, console_manager, game_context):
        self.console_manager = console_manager
        self.game_context = game_context
        self.current_scene = None
        self.scenes = {
            "CharacterCreationScene": CharacterCreationScene,
            "GameScene": GameScene,
            "MainMenuScene": MainMenuScene
        }
        self.transition_to("MainMenuScene")

    def transition_to(self, scene_name):
        self.current_scene = self.scenes[scene_name](self.console_manager, self, self.game_context)

    def render_current_scene(self):
        self.current_scene.render()

    def handle_input(self, key_events, mouse_events):
        self.current_scene.handle_input(key_events, mouse_events)
