from enum import Enum

from clubsandwich.geom import Point
from clubsandwich.ui import RectView

import tdl
from managers.echo import EchoService
from stats.enums import StatsEnum


class GameConsoles(Enum):
    ActionLog = 0
    Status = 1


class GameWindow(RectView):
    def __init__(self, game_context, **kwargs):
        super().__init__(fill=True, **kwargs)
        self.game_context = game_context

    def draw(self, ctx):
        player = self.game_context.player
        current_level = player.location.level
        self.draw_gui(player, ctx)
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
        if player.is_dead():
            EchoService.singleton.standard_context_echo(0, 4, 'You have died!')

    @staticmethod
    def draw_gui(player, ctx):
        ctx.printf(Point(0, 0), "Health: {}\n\n".format(int(player.stats.get_current_value(StatsEnum.Health))))
        ctx.printf(Point(0, 1), "Attack Power: {}\n\n".format(player.get_attack_modifier()))
        ctx.printf(Point(0, 2), "Defense: {}\n\n".format(player.get_armor_class()))
        ctx.printf(Point(0, 3), "Speed: {}\n\n".format(player.get_speed_modifier()))

    @staticmethod
    def draw_map(current_level, viewer_fov, ctx):
        for x, y in viewer_fov:
            if not x >= len(current_level.maze) and not y >= len(current_level.maze[x]):
                ctx.printf(Point(x, y), current_level.maze[x][y].display.get_draw_info())
                current_level.maze[x][y].is_explored = True

    @staticmethod
    def draw_items(player, level, ctx):
        for item in level.spawned_items:
            x, y = item.location.get_local_coords()
            if (x, y) in player.fov:
                ctx.printf(Point(x, y), item.display.get_draw_info())

    @staticmethod
    def draw_characters(player, level, ctx):
        # draw monsters
        for monster in level.spawned_monsters:
            x, y = monster.location.get_local_coords()
            if (x, y) in player.fov:
                ctx.printf(Point(x, y), monster.display.get_draw_info())

    @staticmethod
    def draw_player(player, ctx):
        ctx.printf(
            Point(player.location.local_x, player.location.local_y),
            player.display.get_draw_info()
        )

    @staticmethod
    def set_tiles_background_color(current_level, ctx):
        # TODO Instead of using a different color, we should darken whatever color it is.
        # TODO Allowing us to use many colors as walls and tiles to create levels with different looks.
        for y in range(current_level.height):
            for x in range(current_level.width):
                tile = current_level.maze[x][y]
                wall = tile.block_sight
                ground = tile.is_ground

                if tile.is_explored:
                    if wall:
                        ctx.printf(Point(x, y), '[color=gray]#')
                    elif ground:
                        ctx.printf(Point(x, y), '[color=gray].')

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
