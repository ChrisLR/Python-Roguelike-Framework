from .component import Component
from managers.echo import EchoService
from echo.contexts import Context


class Consumable(Component):
    NAME = "consumable"

    """ A component making an object consumable."""
    def __init__(self, message, effects):
        super().__init__()
        self.message = message
        self.on_consume_effects = effects

    def consume(self, consumer):
        if consumer.effects:
            for effect in self.on_consume_effects:
                consumer.effects.add_effect(effect)

        EchoService.singleton.echo(
            message=self.message,
            context=Context.standard(actor=consumer, target_item=self.host)
        )

