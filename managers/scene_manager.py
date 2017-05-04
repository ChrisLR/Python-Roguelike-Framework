from scenes import (
    CharacterCreationScene,
    GameScene,
    InventoryScene,
    InventoryQueryScene,
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
            "InventoryScene": InventoryScene,
            "InventoryQueryScene": InventoryQueryScene,
            "MainMenuScene": MainMenuScene
        }
        self.scenes_cache = {}
        self.transition_to("MainMenuScene")

    def transition_to(self, scene_name):
        new_scene = self.scenes_cache.get(scene_name, None)
        if not new_scene:
            new_scene = self.scenes[scene_name](self.console_manager, self, self.game_context)
            if new_scene.persistent:
                self.scenes_cache[scene_name] = new_scene
        self.current_scene = new_scene

    def render_current_scene(self):
        self.current_scene.render()

    def handle_input(self, key_events):
        self.current_scene.handle_input(key_events)
