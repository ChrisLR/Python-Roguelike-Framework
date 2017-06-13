from areas.tile import Tile
from components.display import Display
from util.colors import Colors

stone_wall = Tile("stone_wall", 0, 0, Display(Colors.GRAY, Colors.BLACK, "#"), True)
dirt_wall = Tile("dirt_wall", 0, 0, Display(Colors.SADDLE_BROWN, Colors.BLACK, "#"), True)
forest_tree_wall = Tile("forest_tree_wall", 0, 0, Display(Colors.DARK_GREEN, Colors.BLACK, "7"), True)

stone_floor = Tile("stone_floor", 0, 0, Display(Colors.LIGHT_GRAY, Colors.BLACK, "."), False)
dirt_floor = Tile("dirt_floor", 0, 0, Display(Colors.OLIVE, Colors.BLACK, "."), False)
forest_grass_floor = Tile("forest_grass_floor", 0, 0, Display(Colors.DARK_GREEN, Colors.BLACK, "."), False)

tiles = [
    stone_floor,
    stone_wall,
    dirt_floor,
    dirt_wall,
    forest_tree_wall,
    forest_grass_floor
]
