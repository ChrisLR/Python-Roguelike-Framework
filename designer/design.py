import json


class DesignPiece(object):
    def __init__(self):
        self.uid = ""
        self.name = ""
        self.theme_id = ""
        self.size_x = 1
        self.size_y = 1
        # These are intended as arrays, so the id would be accessed with coordinates
        self.tile_ids = []
        self.item_ids = []
        self.character_ids = []
        self.furniture_ids = []

    def json(self):
        return json.dumps(
            {
                'uid': self.uid,
                'name': self.name,
                "theme_id": self.theme_id,
                "size_x": self.size_x,
                "size_y": self.size_y,
                "tile_ids": self.tile_ids,
                "item_ids": self.item_ids,
                "character_ids": self.character_ids,
                "furniture_ids": self.furniture_ids
            }
        )

    @classmethod
    def from_json(cls, uid, name, theme_id, size_x, size_y, tile_ids, item_ids, character_ids, furniture_ids):
        new_instance = DesignPiece()
        new_instance.uid = uid
        new_instance.name = name
        new_instance.theme_id = theme_id
        new_instance.size_x = size_x
        new_instance.size_y = size_y
        new_instance.tile_ids = tile_ids
        new_instance.item_ids = item_ids
        new_instance.character_ids = character_ids
        new_instance.furniture_ids = furniture_ids

        return new_instance
