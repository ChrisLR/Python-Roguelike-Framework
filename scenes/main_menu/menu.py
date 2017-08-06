import cocos
import pyglet
from cocos.director import director
from scenes.character_creation.scene import CharacterCreationScene


class MainMenu(cocos.menu.Menu):
    def __init__(self, title, game_context):
        super().__init__(title)
        width, height = director.get_window_size()
        self.font_title['font_size'] = 10
        self.font_title['width'] = width
        self.font_title['multiline'] = True
        self.font_title['align'] = 'center'
        self.font_item['font_size'] = 10
        self.font_item_selected['font_size'] = 10
        self.create_menu([
            cocos.menu.MenuItem('Start', callback_func=lambda: director.push(CharacterCreationScene(game_context))),
            cocos.menu.MenuItem('Quit', callback_func=lambda: director.pop())
        ])

    def _generate_title(self):
        width, height = director.get_window_size()
        self.font_title['x'] = width // 2
        self.font_title['text'] = self.title
        self.title_label = pyglet.text.Label(**self.font_title)
        self.title_label.y = height - self.title_label.content_height // 2

        pyglet.font.load(self.font_title['font_name'], self.font_title['font_size'])
        self.title_height = self.title_label.content_height

