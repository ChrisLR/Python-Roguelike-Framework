from .component import Component


class Consumable(Component):
    """ A component making an object consumable."""
    def __init__(self):
        super().__init__()
        self.message = ""
        self.on_consume_effects = []

    def consume(self, consumer):
        for effect in self.on_consume_effects:
            effect.apply(consumer)
        self.host.mark_as_destroyed()
