from enum import Enum


class MessageType(Enum):
    ObjectDestroyed = 0


class QueryType(Enum):
    StatModifier = 0
    ExperiencePool = 1

