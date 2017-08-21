import data.python_templates.material
from combat.enums import DamageType
from components.armor import Armor
from components.weapon import Weapon
from components.display import Display
from components.stats import Stats
from stats.enums import Size
from items.item import Item
from items import enums as item_enums
from util.colors import Colors
from util.dice import Dice, DiceStack


def build_short_sword():
    _short_sword = Item(
        uid="short_sword",
        name="Short Sword",
        description="A short sword.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _short_sword.register_component(data.python_templates.material.Iron.copy())
    _short_sword.register_component(Stats(health=1, size=Size.Medium))
    _short_sword.register_component(
        Weapon(weapon_category=item_enums.WeaponCategory.Martial, weapon_type=item_enums.WeaponType.Melee,
               size=Size.Small, melee_damage_type=DamageType.Pierce, melee_damage_dice=DiceStack(1, Dice(6)))
    )

    return _short_sword


def build_long_sword():
    _long_sword = Item(
        uid="long_sword",
        name="Longsword",
        description="A longsword.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _long_sword.register_component(data.python_templates.material.Iron.copy())
    _long_sword.register_component(Stats(health=1, size=Size.Medium))
    _long_sword.register_component(
        Weapon(weapon_category=item_enums.WeaponCategory.Martial, weapon_type=item_enums.WeaponType.Melee,
               size=Size.Medium, melee_damage_type=DamageType.Slash, melee_damage_dice=DiceStack(1, Dice(8)))
    )

    return _long_sword


def build_helmet():
    _helmet = Item(
        uid="helmet",
        name="Helmet",
        description="A helmet.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _helmet.register_component(data.python_templates.material.Iron.copy())
    _helmet.register_component(Stats(health=10, size=Size.Medium, weight=2))
    _helmet.register_component(
        Armor(
            base_armor_class=2,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_head"],
            worn_layer=item_enums.WornLayer.Outer
        )
    )

    return _helmet


def build_leather_hood():
    _item = Item(
        uid="hood",
        name="hood",
        description="A leather hood.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _item.register_component(data.python_templates.material.Leather.copy())
    _item.register_component(Stats(health=10, size=Size.Medium, weight=2))
    _item.register_component(
        Armor(
            base_armor_class=2,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_head"],
            worn_layer=item_enums.WornLayer.Outer
        )
    )

    return _item


def build_breastplate():
    _breastplate = Item(
        uid="breastplate",
        name="Breastplate",
        description="An iron breastplate..",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _breastplate.register_component(data.python_templates.material.Iron.copy())
    _breastplate.register_component(Stats(health=10, size=Size.Medium, weight=4))
    _breastplate.register_component(
        Armor(
            base_armor_class=4,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_torso"],
            worn_layer=item_enums.WornLayer.Outer,
        )
    )

    return _breastplate


def build_leather_cuirass():
    _item = Item(
        uid="cuirass",
        name="Cuirass",
        description="A leather cuirass",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _item.register_component(data.python_templates.material.Leather.copy())
    _item.register_component(Stats(health=10, size=Size.Medium, weight=4))
    _item.register_component(
        Armor(
            base_armor_class=4,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_torso"],
            worn_layer=item_enums.WornLayer.Outer,
        )
    )

    return _item


def build_bracer():
    _bracers = Item(
        uid="bracer",
        name="Bracer",
        description="An iron bracer",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _bracers.register_component(data.python_templates.material.Iron.copy())
    _bracers.register_component(Stats(health=10, size=Size.Medium, weight=0.5))
    _bracers.register_component(
        Armor(
            base_armor_class=0.5,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_arm"],
            worn_layer=item_enums.WornLayer.Outer,
        )
    )

    return _bracers


def build_gauntlet():
    _gauntlet = Item(
        uid="gauntlet",
        name="Gauntlet",
        description="An iron gauntlet",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _gauntlet.register_component(data.python_templates.material.Iron.copy())
    _gauntlet.register_component(Stats(health=10, size=Size.Medium, weight=0.5))
    _gauntlet.register_component(
        Armor(
            base_armor_class=0.5,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_hand"],
            worn_layer=item_enums.WornLayer.Outer,
        )
    )

    return _gauntlet


def build_greave():
    _greave = Item(
        uid="greave",
        name="Greave",
        description="An iron greave",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _greave.register_component(data.python_templates.material.Iron.copy())
    _greave.register_component(Stats(health=10, size=Size.Medium, weight=0.5))
    _greave.register_component(
        Armor(
            base_armor_class=0.5,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_leg"],
            worn_layer=item_enums.WornLayer.Outer,
        )
    )

    return _greave


def build_leather_pants():
    # TODO Some items need to take two slots rather than one.
    item = Item(
        uid="pants",
        name="pants",
        description="Leather pants",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    item.register_component(data.python_templates.material.Leather.copy())
    item.register_component(Stats(health=10, size=Size.Medium, weight=0.5))
    item.register_component(
        Armor(
            base_armor_class=1,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_leg"],
            worn_layer=item_enums.WornLayer.Outer,
        )
    )

    return item


def build_boot():
    _boot = Item(
        uid="boot",
        name="Boot",
        description="An iron boot",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _boot.register_component(data.python_templates.material.Iron.copy())
    _boot.register_component(Stats(health=10, size=Size.Medium, weight=0.5))
    _boot.register_component(
        Armor(
            base_armor_class=0.5,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_foot"],
            worn_layer=item_enums.WornLayer.Outer,
        )
    )

    return _boot


def build_longbow():
    _longbow = Item(
        uid="longbow",
        name="Longbow",
        description="A Longbow",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _longbow.register_component(data.python_templates.material.Wood.copy())
    _longbow.register_component(Stats(health=1, size=Size.Medium))
    _longbow.register_component(
        Weapon(
            weapon_category=item_enums.WeaponCategory.Martial,
            weapon_type=item_enums.WeaponType.Ranged,
            size=Size.Medium,
            melee_damage_type=DamageType.Blunt,
            melee_damage_dice=DiceStack(1, Dice(4)),
            ammunition_uid="arrow",
            normal_range=150,
            long_range=600,
            two_handed=True,
            ranged_damage_type=DamageType.Pierce,
            ranged_damage_dice=DiceStack(1, Dice(8))
        ),

    )

    return _longbow


def build_longbow():
    _longbow = Item(
        uid="longbow",
        name="Longbow",
        description="A Longbow",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _longbow.register_component(data.python_templates.material.Wood.copy())
    _longbow.register_component(Stats(health=1, size=Size.Medium))
    _longbow.register_component(
        Weapon(
            weapon_category=item_enums.WeaponCategory.Martial,
            weapon_type=item_enums.WeaponType.Ranged,
            size=Size.Medium,
            melee_damage_type=DamageType.Blunt,
            melee_damage_dice=DiceStack(1, Dice(4)),
            ammunition_uid="arrow",
            normal_range=150,
            long_range=600,
            two_handed=True,
            ranged_damage_type=DamageType.Pierce,
            ranged_damage_dice=DiceStack(1, Dice(8))
        ),
    )

    return _longbow


def build_dagger():
    _dagger = Item(
        uid="dagger",
        name="Dagger",
        description="A Dagger",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _dagger.register_component(data.python_templates.material.Iron.copy())
    _dagger.register_component(Stats(health=1, size=Size.Small))
    _dagger.register_component(
        Weapon(
            weapon_category=item_enums.WeaponCategory.Simple,
            weapon_type=item_enums.WeaponType.Ranged,
            size=Size.Medium,
            melee_damage_type=DamageType.Pierce,
            melee_damage_dice=DiceStack(1, Dice(4)),
            ammunition_uid="arrow",
            normal_range=20,
            long_range=60,
            ranged_damage_type=DamageType.Pierce,
            ranged_damage_dice=DiceStack(1, Dice(4)),
            finesse=True,
            light=True
        ),
    )

    return _dagger


def build_arrow():
    _arrow = Item(
        uid="arrow",
        name="Arrow",
        description="An arrow",
        display=Display(Colors.DARK_GRAY, Colors.BLACK, "!"),
    )
    _arrow.register_component(data.python_templates.material.Wood.copy())
    _arrow.register_component(Stats(health=1, size=Size.Small))

    return _arrow


short_sword = build_short_sword()
longsword = build_long_sword()
longbow = build_longbow()
dagger = build_dagger()

boot = build_boot()
bracer = build_bracer()
breastplate = build_breastplate()
gauntlet = build_gauntlet()
greave = build_greave()
helmet = build_helmet()
leather_hood = build_leather_hood()
leather_cuirass = build_leather_cuirass()
leather_pants = build_leather_pants()
arrow = build_arrow()

item_templates = {
    short_sword.uid: short_sword,
    longsword.uid: longsword,
    boot.uid: boot,
    bracer.uid: bracer,
    breastplate.uid: breastplate,
    gauntlet.uid: gauntlet,
    greave.uid: greave,
    helmet.uid: helmet,
}
