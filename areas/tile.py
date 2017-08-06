import cocos
from components.game_object import GameObject
from components.location import Location


class Tile(GameObject, cocos.tiles.Tile):
    def __init__(self, uid, x=0, y=0, display=None, is_blocked=False):
        GameObject.__init__(self)
        cocos.tiles.Tile.__init__(self, uid, {}, display.ascii_character if display else '%')
        self.uid = uid
        self.register_component(Location(x, y))
        if display:
            self.register_component(display)
        self.is_blocked = is_blocked
        self.is_explored = False
        self.is_ground = False
        self.contains_object = None
        self.block_sight = is_blocked

    def copy(self, x, y):
        new_tile = Tile(self.uid, is_blocked=self.is_blocked)
        new_tile.is_ground = self.is_ground
        self.copy_to(new_tile)
        new_tile.location.local_x = x
        new_tile.location.local_y = y

        return new_tile
