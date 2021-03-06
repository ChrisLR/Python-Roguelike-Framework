from characters.outfit import Outfit
from data.python_templates import items
from data.python_templates import consumables
from data.python_templates import material


def build_starter_warrior():
    return Outfit(
        "starter_warrior",
        items_worn=[
            items.helmet,
            items.breastplate,
            items.bracer,
            items.bracer,
            items.gauntlet,
            items.gauntlet,
            items.greave,
            items.greave,
            items.boot,
            items.boot,
        ],
        items_held=[
            items.longsword,
        ],
        items_in_inventory=[consumables.bread, consumables.waterskin, consumables.potion_of_healing]
    )


def build_starter_thief():
    leather_bracer_variant = items.bracer.copy()
    leather_bracer_variant.material = material.Leather.copy()
    leather_gauntlet_variant = items.gauntlet.copy()
    leather_gauntlet_variant.material = material.Leather.copy()
    leather_boot_variant = items.boot.copy()
    leather_boot_variant.material = material.Leather.copy()
    return Outfit(
        "starter_thief",
        items_worn=[
            items.leather_hood,
            items.leather_cuirass,
            leather_bracer_variant,
            leather_bracer_variant,
            leather_gauntlet_variant,
            leather_gauntlet_variant.copy(),
            items.leather_pants,
            leather_boot_variant,
            leather_boot_variant.copy(),
        ],
        items_held=[
            items.short_sword,
            items.short_sword.copy()
        ],
        items_in_inventory=[consumables.bread, consumables.waterskin, consumables.potion_of_healing]
    )


def build_starter_ranger():
    leather_bracer_variant = items.bracer.copy()
    leather_bracer_variant.material = material.Leather.copy()
    leather_gauntlet_variant = items.gauntlet.copy()
    leather_gauntlet_variant.material = material.Leather.copy()
    leather_boot_variant = items.boot.copy()
    leather_boot_variant.material = material.Leather.copy()
    arrows = [items.arrow.copy() for i in range(0, 20)]
    return Outfit(
        "starter_ranger",
        items_worn=[
            items.leather_hood,
            items.leather_cuirass,
            leather_bracer_variant,
            leather_bracer_variant,
            leather_gauntlet_variant,
            leather_gauntlet_variant.copy(),
            items.leather_pants,
            leather_boot_variant,
            leather_boot_variant.copy(),
        ],
        items_held=[
            items.longbow,
        ],
        items_in_inventory=[
            consumables.bread,
            consumables.waterskin,
            consumables.potion_of_healing,
            items.dagger, items.dagger.copy(),
            *arrows,
        ]
    )

starter_warrior = build_starter_warrior()
starter_thief = build_starter_thief()
starter_ranger = build_starter_ranger()
outfits = [starter_warrior, starter_thief, starter_ranger]
