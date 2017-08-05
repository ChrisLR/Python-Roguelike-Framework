import cocos
from scenes.character_creation.menu import CharacterCreationMenu


class CharacterCreationUILayer(cocos.layer.Layer):
    def __init__(self, class_templates, race_templates):
        super().__init__()
        self.menu = CharacterCreationMenu(title='Character Creation', class_templates, race_templates)
        self.add(self.menu)

