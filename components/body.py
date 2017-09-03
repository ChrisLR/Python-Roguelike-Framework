import abc
import copy
import logging
import random

import abilities
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
                and abilities.Grasp in bodypart.physical_abilities]

    def get_physical_abilities(self):
        body_abilities = {}
        for bodypart in self.bodyparts:
            if not bodypart.physical_abilities:
                continue

            for ability in bodypart.physical_abilities:
                if ability.name not in body_abilities:
                    body_abilities[ability.name] = ability
                else:
                    if ability.is_stackable:
                        joint_ability = copy.copy(ability)
                        joint_ability.value += body_abilities.pop(ability.name).value
                        body_abilities[ability.name] = joint_ability

                    if body_abilities[ability.name].value < ability.value:
                        body_abilities[ability.name] = ability

        return body_abilities

    def get_ability(self, ability_type, minimum_value=0):
        body_abilities = self.get_physical_abilities()
        ability = body_abilities.get(ability_type.name, None)
        if ability and ability.value >= minimum_value:
            return ability

    def replace_body_part(self, old_body_part, new_body_part):
        self.bodyparts.remove(old_body_part)
        for bodypart in self.bodyparts:
            if old_body_part in bodypart.child_inserts:
                bodypart.child_inserts.remove(old_body_part)
                bodypart.child_inserts.append(new_body_part)

            if old_body_part in bodypart.child_attachments:
                bodypart.child_attachments.remove(old_body_part)
                bodypart.child_attachments.append(new_body_part)

        new_body_part.child_inserts = old_body_part.child_inserts
        new_body_part.child_attachments = old_body_part.child_attachments
        self.bodyparts.append(new_body_part)
