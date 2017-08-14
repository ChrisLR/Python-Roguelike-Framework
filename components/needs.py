from .component import Component
from components.messages import MessageType
from managers.echo import EchoService


class Needs(Component):
    def __init__(self, needs, metabolism, maximum_points):
        super().__init__()
        self.needs = needs
        self.metabolism = metabolism
        self.current_points = maximum_points.copy()
        self.maximum_points = maximum_points
        self.tick = 10
        self.last_threshold = maximum_points.copy()

    def on_register(self, host):
        super().on_register(host)
        host.register_observer(self, MessageType.AlterNeed, self.alter_need)

    def _get_threshold_percent(self, need):
        return round(self.current_points[need] * 100 / self.maximum_points[need])

    def alter_need(self, need_altered, potency):
        if need_altered in self.needs:
            if potency > 0:
                if self.current_points[need_altered] + potency < self.maximum_points[need_altered]:
                    self.current_points[need_altered] += potency
                else:
                    self.current_points[need_altered] = self.maximum_points[need_altered]
                self.echo_positive(need_altered)
            elif potency < 0:
                if self.current_points[need_altered] - potency > -self.maximum_points[need_altered]:
                    self.current_points[need_altered] -= potency
                else:
                    self.current_points[need_altered] = -self.maximum_points[need_altered]
                self.echo_negative(need_altered)

    def echo_positive(self, need):
        current_percent = self._get_threshold_percent(need)
        for threshold, message in need.positive_threshold_messages.items():
            if self.last_threshold[need] <= threshold <= current_percent:
                EchoService.singleton.echo(message=message)
                self.last_threshold[need] = threshold
                break

    def echo_negative(self, need):
        current_percent = self._get_threshold_percent(need)
        for threshold, message in need.negative_threshold_messages.items():
            if self.last_threshold[need] > threshold >= current_percent:
                EchoService.singleton.echo(message=message)
                self.last_threshold[need] = threshold
                break

    def update(self):
        if self.tick:
            self.tick -= 1
            return

        self.tick = 10
        for need in self.needs:
            cost = 1 * self.metabolism[need]
            if not self.current_points[need] <= -self.maximum_points[need]:
                self.current_points[need] -= cost

            self.echo_negative(need)

    @classmethod
    def create_standard(cls, metabolism, maximum_points, *args):
        """
        Creates a standard needs component from arguments.
        :param metabolism: int Modifier to drain per minute
        :param maximum_points: int Maximum points pool for needs
        :param args: need All needs to initialize.
        :return: Instance of component
        """
        _metabolism = {}
        _maximum_points = {}
        for need in args:
            _metabolism[need] = metabolism
            _maximum_points[need] = maximum_points

        return Needs(
            needs=args,
            metabolism=_metabolism,
            maximum_points=_maximum_points
        )

