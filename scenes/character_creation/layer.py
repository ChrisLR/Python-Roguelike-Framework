import cocos
from scenes.character_creation.menu import CharacterCreationMenu


class CharacterCreationUILayer(cocos.layer.Layer):
    def __init__(self, game_context):
        super().__init__()
        self.menu = CharacterCreationMenu('Character Creation', game_context)
        self.add(self.menu)

