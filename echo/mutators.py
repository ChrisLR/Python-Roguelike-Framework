import abc
from echo.functions import his_her_it, him_her_it, he_her_it


class ContextMutator(object):
    @abc.abstractclassmethod
    def suffix(self):
        pass

    @abc.abstractclassmethod
    def mutator_function(self):
        pass

    @classmethod
    def mutate(cls, value):
        return cls.mutator_function(value)


class His(ContextMutator):
    suffix = "his"
    mutator_function = his_her_it


class Him(ContextMutator):
    suffix = "him"
    mutator_function = him_her_it


class He(ContextMutator):
    suffix = "he"
    mutator_function = he_her_it


listing = [His, Him, He]
