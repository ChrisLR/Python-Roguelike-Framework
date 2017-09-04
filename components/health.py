from components.component import Component
import random


class Health(Component):
    NAME = 'health'
    """
    This is the component that implements Health.
    """

    def __init__(self, enforce_maximum):
        super().__init__()
        self.enforce_maximum = enforce_maximum
        self.max_hit_dice = []
        self.current_hit_dice = []
        self.current = 0
        self._base_max_health = 0
        self.maximum_modifiers = []

    @property
    def max(self):
        return self._base_max_health + sum(self.maximum_modifiers)

    def register_modifier(self, health_modifier):
        self.maximum_modifiers.append(health_modifier)

    def unregister_modifier(self, health_modifier):
        self.maximum_modifiers.remove(health_modifier)

    def on_register(self, host):
        if host.experience_pool:
            level = host.experience_pool.total_level
        else:
            level = 1

        if host.character_class:
            hit_die = host.character_class.hit_die
        else:
            hit_die = 1

        if host.stats:
            constitution_bonus = host.stats.constitution.modifier
        else:
            constitution_bonus = 0

        self.max_hit_dice = [hit_die for _ in range(0, level)]
        self.current_hit_dice = self.max_hit_dice.copy()
        if not self.enforce_maximum:
            maximum_health = sum((random.randint(1, hit_die) + constitution_bonus) for _ in range(0, level))
        else:
            maximum_health = hit_die * level
            if constitution_bonus:
                maximum_health += constitution_bonus * level

        self._base_max_health = maximum_health
        self.current = maximum_health

    def copy(self):
        return Health(self.enforce_maximum)
