from factories.item_factory import ItemFactory
from components.display import Display
from data.python_templates.effects import restore_health
from util.colors import Colors


bread = ItemFactory.create_food("Bread", description="A loaf of bread.", nutrition_value=50)
bread.register_component(Display(Colors.DARK_BROWN, Colors.BLACK_COLOR, "!"))
waterskin = ItemFactory.create_drink("Waterskin", description="A waterskin filled with water.", nutrition_value=50)
waterskin.register_component(Display(Colors.DARK_BLUE, Colors.BLACK_COLOR, "!"))
potion_of_healing = ItemFactory.create_drink(
    "Potion of healing", description="Potion that heals you.", nutrition_value=0, extra_effects=[restore_health])
potion_of_healing.register_component(Display(Colors.DARK_RED, Colors.BLACK_COLOR, "!"))
