from .component import Component


class Location(Component):
    NAME = "location"

    def __init__(self):
        super().__init__()
        # TODO THIS HOLDS ALL THE INFORMATION NEEDED TO LOCATE SOMETHING
        self.local_x = 0
        self.local_y = 0
        self.global_x = 0
        self.global_y = 0
        self.area = None
        self.level = None

    def copy(self):
        new_instance = Location()
        new_instance.local_x = self.local_x
        new_instance.local_y = self.local_y
        new_instance.global_x = self.global_x
        new_instance.global_y = self.global_y
        new_instance.area = self.area
        new_instance.level = self.level
        return new_instance

    def get_local_coords(self):
        return self.local_x, self.local_y
