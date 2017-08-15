from enum import Enum
import tdl
from clubsandwich.geom import Point, Size
from clubsandwich.ui import RectView

from managers.echo import EchoService
from stats.enums import StatsEnum
from ui.camera import Camera


class GameWindow(RectView):
    def __init__(self, game_context, **kwargs):
        super().__init__(fill=True, **kwargs)
        self.game_context = game_context
        player = self.game_context.player
        self.camera = Camera(location=player.location.copy(), screen_size=Size(120, 30))

    def draw(self, ctx):
        player = self.game_context.player
        current_level = player.location.level
        self.camera.focus_on_game_object(player)
        self.set_tiles_background_color(ctx)

        player_x = player.location.local_x
        player_y = player.location.local_y

        def is_transparent_callback(x, y):
            if x <= 0 or y <= 0:
                return False
            return self.is_transparent(current_level, x, y)

        player.fov = tdl.map.quickFOV(player_x, player_y, is_transparent_callback, 'basic')

        # NB: Order in which things are render is important
        self.draw_map(player.fov, ctx)
        self.draw_items(player, ctx)
        self.draw_characters(player, ctx)
        self.draw_player(player, ctx)

    def draw_map(self, viewer_fov, ctx):
        current_level = self.camera.location.level

        for x, y in viewer_fov:
            if not x >= len(current_level.maze) and not y >= len(current_level.maze[x]):
                relative_point = self.camera.transform(Point(x, y))
                if relative_point is not None:
                    ctx.printf(
                        relative_point,
                        current_level.maze[x][y].display.get_draw_info()
                    )
                    current_level.maze[x][y].is_explored = True

    def draw_items(self, player, ctx):
        current_level = self.camera.location.level
        for item in current_level.spawned_items:
            x, y = item.location.get_local_coords()
            if (x, y) in player.fov:
                relative_point = self.camera.transform(Point(x, y))
                if relative_point is not None:
                    ctx.printf(
                        relative_point,
                        item.display.get_draw_info()
                    )

    def draw_characters(self, player, ctx):
        # draw monsters
        current_level = self.camera.location.level
        for monster in current_level.spawned_monsters:
            x, y = monster.location.get_local_coords()
            if (x, y) in player.fov:
                relative_point = self.camera.transform(Point(x, y))
                if relative_point is not None:
                    ctx.printf(
                        relative_point,
                        monster.display.get_draw_info()
                    )

    def draw_player(self, player, ctx):
        relative_point = self.camera.transform(Point(*player.location.get_local_coords()))
        if relative_point is not None:
            ctx.printf(relative_point, player.display.get_draw_info())

    def set_tiles_background_color(self, ctx):
        # TODO Instead of using a different color, we should darken whatever color it is.
        # TODO Allowing us to use many colors as walls and tiles to create levels with different looks.
        current_level = self.camera.location.level
        for y in range(current_level.height):
            for x in range(current_level.width):
                relative_point = self.camera.transform(Point(x, y))
                if relative_point is not None:
                    tile = current_level.maze[x][y]
                    wall = tile.block_sight
                    ground = tile.is_ground

                    if tile.is_explored:
                        if wall:
                            ctx.printf(relative_point, '[color=gray]#')
                        elif ground:
                            ctx.printf(relative_point, '[color=gray].')

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
