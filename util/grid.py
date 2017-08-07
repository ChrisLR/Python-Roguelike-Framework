import cocos


class Grid(object):
    def __init__(self, width, height):
        self.objects = [[cocos.tiles.RectCell(x, y, 10, 10, properties={}, tile=None)
                        for y in range(height)] for x in range(width)]

    def place(self, game_object, x, y):
        self.objects[x][y].tile = game_object

    def move_to(self, game_object, x, y):
        self.objects[x][y].tile = None
        self.place(game_object, x, y)

    def __getitem__(self, key):
        return self.objects[key]

    def __len__(self):
        return len(self.objects)
