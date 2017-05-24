from areas.tile import Tile
from components.display import Display
from util.colors import Colors

stone_wall_tile = Tile(0, 0, Display(Colors.GRAY, Colors.BLACK, "#"), True)
dirt_wall_tile = Tile(0, 0, Display(Colors.SADDLE_BROWN, Colors.BLACK, "#"), True)


stone_floor_tile = Tile(0, 0, Display(Colors.LIGHT_GRAY, Colors.BLACK, "."), False)
dirt_floor_tile = Tile(0, 0, Display(Colors.OLIVE, Colors.BLACK, "."), False)
