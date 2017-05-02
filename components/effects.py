from .component import Component

# TODO Anything could have an EFFECTS component
# TODO This component would keep active effects and respond to queries about modifiers.
# TODO It could also apply effects itself, like damage or healing.
# TODO It should be called in a sort of update loop.


class Effects(Component):
    NAME = "effects"

    def __init__(self):
        super().__init__()
        self.active_effects = {}

    def add_effect(self, effect):
        if effect in self.active_effects:
            if effect.stack:
                self.active_effects[effect] += effect.duration
            else:
                self.active_effects[effect] = effect.duration
        else:
            self.active_effects[effect] = effect.duration
            effect.on_start(self.host)

    def update(self):
        finished_effects = []
        for effect in self.active_effects.keys():
            effect.update(self.host)
            self.active_effects[effect] -= 1
            if self.active_effects[effect] <= 0:
                finished_effects.append(effect)

        for finished_effect in finished_effects:
            finished_effect.on_end(self.host)
            del self.active_effects[finished_effect]
