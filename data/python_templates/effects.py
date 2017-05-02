from effects.effect import AlterNeedEffect, AlterStatEffect
from stats.enums import StatsEnum
from data.python_templates import needs


restore_hunger = AlterNeedEffect(
    "restore_hunger", "Restore Hunger",
    need_altered=needs.hunger, duration=1, potency=10
)
restore_thirst = AlterNeedEffect(
    "restore_thirst", "Restore Thirst",
    need_altered=needs.thirst, duration=1, potency=10
)
restore_health = AlterStatEffect(
    "restore_health", "Restore Health",
    stat_altered=StatsEnum.Health, duration=5, potency=2
)
