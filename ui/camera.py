from clubsandwich.geom import Point, Rect, Size


class Camera(object):
    def __init__(self, location, screen_size):
        """
        Initialize a Camera for drawing.
        :param location: Location component
        :param screen_bounds: Size(width, height) of the boundaries of the screen on which to draw.
        """
        self.location = location
        self.screen_point_offset = Point(1, -10)
        self.screen_size = Size(
            screen_size.width - self.screen_point_offset.x,
            screen_size.height - self.screen_point_offset.y
        )
        self.point = Point(*self.location.get_local_coords())
        self.view_rect = Rect(self.point, self.screen_size)

    def transform(self, point, enforce_bounds=True):
        """
        Transforms an absolute Point(x, y) to it's relative Point(x, y)
        :param point: Absolute Point(x, y) to transform
        :param enforce_bounds: If True we will return None if it is out of bounds.
        :return: Relative Point to draw
        """
        if enforce_bounds:
            if not self.check_bounds(point.x, point.y):
                return None

        return Point(point.x - self.point.x, point.y - self.point.y)

    def focus_on_game_object(self, game_object):
        self.location.area = game_object.location.area
        self.location.level = game_object.location.level
        self.location.global_x = game_object.location.global_x
        self.location.global_y = game_object.location.global_y
        self.location.local_x = game_object.location.local_x - int(self.screen_size.width / 2)
        self.location.local_y = game_object.location.local_y - int(self.screen_size.height / 2)
        self.point = Point(*self.location.get_local_coords())
        self.view_rect = Rect(self.point, self.screen_size)

    def check_bounds(self, x=None, y=None):
        """
        Allows checking the X or the Y or both to see if its in drawing bounds.
        """
        if x is not None:
            if self.point.x > x or self.point.x + self.screen_size.width < x:
                return False

        if y is not None:
            if self.point.y > y or self.point.y + self.screen_size.width < y:
                return False

        return True

