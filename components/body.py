import abc
import logging
import random

from abilities.physical_abilities import PhysicalAbilities
from combat.enums import ThreatLevel
from components.component import Component

logger_ = logging.getLogger()


class Body(Component):
    NAME = "body"
    """
    Height is in feet, Weight in pounds
    """
    @abc.abstractclassmethod
    def uid(self):
        pass

    @abc.abstractclassmethod
    def name(self):
        pass

    @abc.abstractclassmethod
    def base_height(self):
        pass

    @abc.abstractclassmethod
    def base_weight(self):
        pass

    @abc.abstractclassmethod
    def template_outer_material(self):
        pass

    @abc.abstractclassmethod
    def template_inner_material(self):
        pass

    @abc.abstractclassmethod
    def template_structural_material(self):
        pass

    @abc.abstractclassmethod
    def template_blood(self):
        pass

    def __init__(self, bodyparts):
        super().__init__()
        self.outer_material = self.template_outer_material.copy()
        self.inner_material = self.template_inner_material.copy()
        self.structural_material = self.template_structural_material.copy()
        self.blood = self.template_blood()
        self.bodyparts = bodyparts

    def copy(self):
        return type(self)()

    def __str__(self):
        return "Body({})".format(self.name)

    def get_body_part(self, uid):
        return next((bodypart for bodypart in self.bodyparts if bodypart.uid == uid))

    def get_body_parts(self, uid):
        return [bodypart for bodypart in self.bodyparts if bodypart.uid == uid]

    @staticmethod
    def _random_roll_body_part(bodyparts):
        tries = 0
        max_tries = 3
        while tries < max_tries:
            tries += 1
            for bodypart in bodyparts:
                if random.randrange(0, 100) <= bodypart.relative_size:
                    return bodypart

        return random.choice(bodyparts)

    def get_random_body_part_for_threat_level(self, threat_level):
        size_sorted_body_parts = [bodypart for bodypart in self.bodyparts
                                  if bodypart.threat_level == threat_level]
        if not size_sorted_body_parts:
            if threat_level < ThreatLevel.Fatal:
                return self.get_random_body_part_for_threat_level(ThreatLevel[threat_level.value + 1])
            else:
                return self.get_random_body_part_by_relative_size()

        return self._random_roll_body_part(size_sorted_body_parts)

    def get_random_body_part_by_relative_size(self):
        size_sorted_body_parts = sorted(self.bodyparts, key=lambda bodypart: bodypart.relative_size, reverse=True)

        return self._random_roll_body_part(size_sorted_body_parts)

    def get_grasp_able_body_parts(self):
        return [bodypart for bodypart in self.bodyparts
                if bodypart.physical_abilities
                and PhysicalAbilities.GRASP in bodypart.physical_abilities]

    def get_physical_abilities(self):
        abilities = {}
        for bodypart in self.bodyparts:
            if not bodypart.physical_abilities:
                continue

            for ability_name, ability_value in bodypart.physical_abilities.items():
                if ability_name not in abilities:
                    abilities[ability_name] = ability_value
                else:
                    if abilities[ability_name] < ability_value:
                        abilities[ability_name] = ability_value

        return abilities
