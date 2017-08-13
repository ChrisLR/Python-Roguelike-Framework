from enum import Enum
import bearlibterminal
import settings
import tdl
from settings import DUNGEON_COLORS as COLORS
from stats.enums import StatsEnum
from ui.windows import SingleWindow
from clubsandwich.ui import RectView
from clubsandwich.geom import Point


class GameConsoles(Enum):
    ActionLog = 0
    Status = 1


class GameWindow(RectView):
    def __init__(self, game_context, **kwargs):
        super().__init__(fill=True, **kwargs)
        self.game_context = game_context
        # TODO Eventually we want to map more than just movement keys
        self.movement_keys = settings.KEY_MAPPINGS

    def draw(self, ctx):
        player = self.game_context.player
        current_level = player.location.level
        self.draw_gui(player, ctx)
        # self.set_tiles_background_color(current_level, ctx)
        #
        # player_x = player.location.local_x
        # player_y = player.location.local_y
        #
        # def is_transparent_callback(x, y):
        #     if x <= 0 or y <= 0:
        #         return False
        #     return self.is_transparent(current_level, x, y)
        #
        # player.fov = tdl.map.quickFOV(player_x, player_y, is_transparent_callback, 'basic')
        # # NB: Order in which things are render is important
        # self.draw_map(current_level, player.fov, ctx)
        # self.draw_items(player, current_level, ctx)
        # self.draw_characters(player, current_level, ctx)
        # self.draw_player(player, ctx)
        # if player.is_dead():
        #     self.game_context.echo_service.standard_context_echo(0, 4, 'You have died!')

    def draw_gui(self, player, ctx):
        ctx.printf(Point(0, 2), "Health: {}\n\n".format(int(player.stats.get_current_value(StatsEnum.Health))))
        ctx.printf(Point(0, 5), "Attack Power: {}\n\n".format(player.get_attack_modifier()))
        ctx.printf(Point(0, 8), "Defense: {}\n\n".format(player.get_armor_class()))
        ctx.printf(Point(0, 11), "Speed: {}\n\n".format(player.get_speed_modifier()))

    def draw_map(self, current_level, viewer_fov, ctx):
        for x, y in viewer_fov:
            if not x >= len(current_level.maze) and not y >= len(current_level.maze[x]):
                self.main_console.drawChar(x, y, **current_level.maze[x][y].display.get_draw_info())
                current_level.maze[x][y].is_explored = True

    def draw_items(self, player, level, ctx):
        for item in level.spawned_items:
            x, y = item.location.get_local_coords()
            if (x, y) in player.fov:
                self.main_console.drawChar(x, y, **item.display.get_draw_info())

    def draw_characters(self, player, level, ctx):
        # draw monsters
        for monster in level.spawned_monsters:
            x, y = monster.location.get_local_coords()
            if (x, y) in player.fov:
                self.main_console.drawChar(x, y, **monster.display.get_draw_info())

    def draw_player(self, player, ctx):
        self.main_console.drawChar(
            player.location.local_x,
            player.location.local_y,
            **player.display.get_draw_info()
        )

    # def handle_input(self, key_events, mouse_events):
    #     """
    #     Any keyboard interaction from the user occurs here
    #     """
    #     super().handle_input(key_events, mouse_events)
    #     player = self.game_context.player
    #     current_level = player.location.level
    #     moved = False
    #
    #     for key_event in key_events:
    #         if key_event.type == 'KEYDOWN':
    #             # TODO Make stairs system to go up or down
    #             # TODO Add Action to pick up items
    #             # TODO We will need to implement an action mapping
    #
    #             # We mix special keys with normal characters so we use keychar.
    #             if not player.is_dead():
    #                 if key_event.key == 'KP5' or key_event.key == '.':
    #                     moved = True
    #
    #                 if key_event.keychar.upper() in self.movement_keys:
    #                     key_x, key_y = self.movement_keys[key_event.keychar.upper()]
    #                     # TODO MANAGERS SHOULD BE IN THE GAME CONTEXT AND ACCESSED FROM IT, NOT GAME SCENE
    #                     self.game_context.action_manager.move_or_attack(player, key_x, key_y)
    #                     moved = True
    #
    #                 if moved:
    #                     player.update()
    #                     for monster in current_level.spawned_monsters:
    #                         monster.update()
    #                         self.game_context.action_manager.monster_take_turn(monster, player)
    #                     moved = False

    def set_tiles_background_color(self, current_level, ctx):
        # TODO Instead of using a different color, we should darken whatever color it is.
        # TODO Allowing us to use many colors as walls and tiles to create levels with different looks.
        for y in range(current_level.height):
            for x in range(current_level.width):
                tile = current_level.maze[x][y]
                wall = tile.block_sight
                ground = tile.is_ground

                if tile.is_explored:
                    if wall:
                        self.main_console.drawChar(x, y, '#', fgcolor=COLORS['dark_gray_wall'])
                    elif ground:
                        self.main_console.drawChar(x, y, '.', fgcolor=COLORS['dark_ground'])

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
