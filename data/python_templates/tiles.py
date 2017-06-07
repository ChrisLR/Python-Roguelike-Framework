from areas.tile import Tile
from components.display import Display
from util.colors import Colors

stone_wall = Tile(0, 0, Display(Colors.GRAY, Colors.BLACK, "#"), True)
dirt_wall = Tile(0, 0, Display(Colors.SADDLE_BROWN, Colors.BLACK, "#"), True)
forest_tree_wall = Tile(0, 0, Display(Colors.DARK_GREEN, Colors.BLACK, "7"), True)

stone_floor = Tile(0, 0, Display(Colors.LIGHT_GRAY, Colors.BLACK, "."), False)
dirt_floor = Tile(0, 0, Display(Colors.OLIVE, Colors.BLACK, "."), False)
forest_grass_floor = Tile(0, 0, Display(Colors.DARK_GREEN, Colors.BLACK, "."), False)

