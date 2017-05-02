from factories.item_factory import ItemFactory
from data.python_templates.effects import restore_health


bread = ItemFactory.create_food("Bread", description="A loaf of bread.", nutrition_value=50)
waterskin = ItemFactory.create_drink("Waterskin", description="A waterskin filled with water.", nutrition_value=50)
potion_of_healing = ItemFactory.create_drink(
    "Potion of healing", description="Potion that heals you.", nutrition_value=0, extra_effects=[restore_health])
