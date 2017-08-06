import cocos

from scenes.character_creation.layer import CharacterCreationUILayer


class CharacterCreationScene(cocos.scene.Scene):
    ID = "CharacterCreation"
    # TODO Remake this properly using the new style controls interface.
    
    def __init__(self, game_context):
        self.layer = CharacterCreationUILayer(game_context)
        super().__init__(self.layer)
