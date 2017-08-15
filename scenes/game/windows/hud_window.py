from clubsandwich.geom import Point
from clubsandwich.ui import RectView

from stats.enums import StatsEnum


class HudWindow(RectView):
    def __init__(self, game_context, **kwargs):
        super().__init__(fill=True, **kwargs)
        self.game_context = game_context

    def draw(self, ctx):
        player = self.game_context.player
        self.draw_gui(player, ctx)

    @staticmethod
    def draw_gui(player, ctx):
        ctx.printf(Point(0, 0), "Health: {}\n\n".format(int(player.stats.get_current_value(StatsEnum.Health))))
        ctx.printf(Point(0, 1), "Attack Power: {}\n\n".format(player.get_attack_modifier()))
        ctx.printf(Point(0, 2), "Defense: {}\n\n".format(player.get_armor_class()))
        ctx.printf(Point(0, 3), "Speed: {}\n\n".format(player.get_speed_modifier()))
