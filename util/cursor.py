from components.game_object import GameObject
from components.display import Display
from util.colors import Colors


class Cursor(GameObject):
    system_ghost = True

    def __init__(self, location, callback, *callback_args, **callback_kwargs):
        super().__init__()
        self.register_component(location)
        self.display = Display(Colors.YELLOW, Colors.BLACK, "X")
        self.callback = callback
        self.callback_args = callback_args
        self.callback_kwargs = callback_kwargs

    def on_enter(self):
        monster = self.get_monster()
        if monster:
            self.recall(monster)

    def get_monster(self):
        return next((monster for monster in self.location.level.monster_spawn_list
                     if monster.location.local_x == self.location.local_x
                     and monster.location.local_y == self.location.local_y), None)

    def recall(self, monster):
        self.callback(monster, *self.callback_args, **self.callback_kwargs)
