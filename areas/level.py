from util.grid import Grid


class Level(object):
    def __init__(self, width, height):
        # Permanent variables
        self.name = ""
        self.description = ""
        self.max_room_size = 0
        self.min_room_size = 0
        self.max_rooms = 0
        self.width = width
        self.height = height
        self.monster_spawn_list = []
        self.item_spawn_list = []

        # Generated variables
        self.num_rooms = 0
        self.tiles = []
        self.rooms = []
        self.spawned_monsters = []
        self.spawned_items = []

        self.object_cell_grid = Grid(width, height)





