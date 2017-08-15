from enum import Enum

from clubsandwich.geom import Point
from clubsandwich.ui import RectView

import tdl
from managers.echo import EchoService
from stats.enums import StatsEnum


class GameWindow(RectView):
    def __init__(self, game_context, **kwargs):
        super().__init__(fill=True, **kwargs)
        self.game_context = game_context
        self.center_x = 60
        self.center_y = 15
        self.draw_area_minimum, self.draw_area_maximum = GameWindow.get_draw_minimum_maximum(
            self.center_x, self.center_y)

    def draw(self, ctx):
        player = self.game_context.player
        current_level = player.location.level
        self.set_tiles_background_color(current_level, ctx)

        player_x = player.location.local_x
        player_y = player.location.local_y

        def is_transparent_callback(x, y):
            if x <= 0 or y <= 0:
                return False
            return self.is_transparent(current_level, x, y)

        player.fov = tdl.map.quickFOV(player_x, player_y, is_transparent_callback, 'basic')
        # NB: Order in which things are render is important
        self.draw_map(current_level, player.fov, ctx)
        self.draw_items(player, current_level, ctx)
        self.draw_characters(player, current_level, ctx)
        self.draw_player(player, ctx)

    def draw_map(self, current_level, viewer_fov, ctx):
        # Okay so the map would be like 10 squares under the gui.
        # We'd need a good 10 squares for the log, maybe more.
        # That leaves 30 square
        # We need to transform the Y to -30 and not draw anything beyond.

        for x, y in viewer_fov:
            if not x >= len(current_level.maze) and not y >= len(current_level.maze[x]):
                if self.check_bounds(x, y):
                    relative_point = self.get_relative_location(x, y)
                    ctx.printf(
                        relative_point,
                        current_level.maze[x][y].display.get_draw_info()
                    )
                    current_level.maze[x][y].is_explored = True

    def draw_items(self, player, level, ctx):
        for item in level.spawned_items:
            x, y = item.location.get_local_coords()
            if self.check_bounds(x, y):
                if (x, y) in player.fov:
                    relative_point = self.get_relative_location(x, y)
                    ctx.printf(
                        relative_point,
                        item.display.get_draw_info()
                    )

    def draw_characters(self, player, level, ctx):
        # draw monsters
        for monster in level.spawned_monsters:
            x, y = monster.location.get_local_coords()
            if self.check_bounds(x, y):
                if (x, y) in player.fov:
                    relative_point = self.get_relative_location(x, y)
                    ctx.printf(
                        relative_point,
                        monster.display.get_draw_info()
                    )

    def draw_player(self, player, ctx):
        ctx.printf(
            Point(self.center_x, self.center_y),
            player.display.get_draw_info()
        )

    def set_tiles_background_color(self, current_level, ctx):
        # TODO Instead of using a different color, we should darken whatever color it is.
        # TODO Allowing us to use many colors as walls and tiles to create levels with different looks.

        for y in range(current_level.height):
            for x in range(current_level.width):
                if not self.check_bounds(x, y):
                    continue

                relative_point = self.get_relative_location(x, y)
                tile = current_level.maze[x][y]
                wall = tile.block_sight
                ground = tile.is_ground

                if tile.is_explored:
                    if wall:
                        ctx.printf(relative_point, '[color=gray]#')
                    elif ground:
                        ctx.printf(relative_point, '[color=gray].')

    @staticmethod
    def get_draw_minimum_maximum(center_x, center_y):
        draw_area_minimum = Point(center_x - 60, center_y - 15)
        draw_area_maximum = Point(center_x + 60, center_y + 15)

        return draw_area_minimum, draw_area_maximum

    def get_relative_location(self, absolute_x, absolute_y):
        bottom_left_x, bottom_left_y = self.center_x - 60, self.center_y - 15
        return Point(absolute_x - bottom_left_x, absolute_y - bottom_left_y)

    def check_bounds(self, absolute_x, absolute_y):
        if self.draw_area_minimum.x < absolute_x < self.draw_area_maximum.x:
            if self.draw_area_minimum.y < absolute_y < self.draw_area_maximum.y:
                return True
        return False

    @staticmethod
    def is_transparent(current_level, x, y):
        """
        Used by map.quickFOV to determine which tile fall within the players "field of view"
        """
        try:
            # Pass on IndexErrors raised for when a player gets near the edge of the screen
            # and tile within the field of view fall out side the bounds of the maze.
            tile = current_level.maze[x][y]
            if tile.block_sight and tile.is_blocked:
                return False
            else:
                return True
        except IndexError:
            return False
