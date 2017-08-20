import abc


class Target(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def targets(self):
        pass


class Single(Target):
    __slots__ = ['_target']

    def __init__(self, target):
        self._target = target

    def targets(self):
        return self._target,


class Cone(Target):
    __slots__ = ['origin', 'direction', 'range', '_targets']

    def __init__(self, origin, direction, range):
        self.origin = origin
        self.direction = direction
        self.range = range
        self._targets = self.get_cone_targets()

    def get_cone_targets(self):
        pass

    def targets(self):
        return self._targets


class Radius(Target):
    __slots__ = ['center', 'range', '_targets']

    def __init__(self, center, range):
        self.center = center
        self.range = range
        self._targets = self.get_radius_targets()

    def get_radius_targets(self):
        pass

    def targets(self):
        return self._targets


class Beam(Target):
    __slots__ = ['origin', 'direction', 'range', '_targets']

    def __init__(self, origin, direction, range):
        self.origin = origin
        self.direction = direction
        self.range = range
        self._targets = self.get_beam_targets()

    def get_beam_targets(self):
        pass

    def targets(self):
        return self._targets
