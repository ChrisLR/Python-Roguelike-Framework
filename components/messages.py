from enum import Enum


class MessageType(Enum):
    ObjectDestroyed = 0
    AlterStat = 1
    AlterNeed = 2


class QueryType(Enum):
    StatModifier = 0
    ExperiencePool = 1

