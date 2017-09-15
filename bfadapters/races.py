from bflib.characters.classes.level import Level
from components.game_object import GameObject
from bflib.characters import races as lib_races
from bflib.characters.races.base import Race as BFRace


class Race(GameObject, BFRace):
    def __init__(self):
        super().__init__()


class Human(Race, lib_races.Human):
    pass
