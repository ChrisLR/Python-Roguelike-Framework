from .component import Component
from managers.echo import EchoService


class Consumable(Component):
    NAME = "consumable"

    """ A component making an object consumable."""
    def __init__(self, message, effects):
        super().__init__()
        self.message = message
        self.on_consume_effects = effects

    def consume(self, consumer):
        for effect in self.on_consume_effects:
            effect.apply(consumer)
        EchoService.singleton.standard_context_echo(message=self.message, actor=consumer, target_item=self.host)
        self.host.mark_as_destroyed()
