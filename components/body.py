import abc
import logging
import random

from abilities.physical_abilities import PhysicalAbilities
from bodies.body_part_tree import BodypartTree
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
    def template_bodypart_tree(self):
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

    def __init__(self):
        super().__init__()
        self.bodypart_tree = self.template_bodypart_tree.copy()
        self.outer_material = self.template_outer_material.copy()
        self.inner_material = self.template_inner_material.copy()
        self.structural_material = self.template_structural_material.copy()
        self.blood = self.template_blood.copy()

    def copy(self):
        return type(self)()

    def __str__(self):
        return "Body({})".format(self.name)

    def get_body_part(self, uid):
        for node in self.bodypart_tree.nodes:
            if node.instance.uid == uid:
                return node.instance

    def get_body_parts(self, uid):
        body_parts = []
        for node in self.bodypart_tree.nodes:
            if not node.instance:
                print("WTF")
            else:
                if node.instance.uid == uid:
                    body_parts.append(node.instance)

        return body_parts

    @staticmethod
    def _random_roll_body_part(body_parts):
        tries = 0
        max_tries = 3
        while tries < max_tries:
            tries += 1
            for node in body_parts:
                if random.randrange(0, 100) <= node.instance.relative_size:
                    return node

        return random.choice(body_parts)

    def get_random_body_part_for_threat_level(self, threat_level):
        size_sorted_body_parts = [node for node in self.bodypart_tree.nodes
                                  if node.instance.threat_level == threat_level]
        if not size_sorted_body_parts:
            if threat_level < ThreatLevel.Fatal:
                return self.get_random_body_part_for_threat_level(ThreatLevel[threat_level.value + 1])
            else:
                return self.get_random_body_part_by_relative_size()

        return self._random_roll_body_part(size_sorted_body_parts)

    def get_random_body_part_by_relative_size(self):
        size_sorted_body_parts = sorted([node for node in self.bodypart_tree.nodes
                                         if node.connection_type == BodypartTree.CONNECTION_TYPE_ATTACHED],
                                        key=lambda node: node.instance.relative_size, reverse=True)

        return self._random_roll_body_part(size_sorted_body_parts)

    def get_grasp_able_body_parts(self):
        return [node.instance for node in self.bodypart_tree.nodes
                if PhysicalAbilities.GRASP in node.instance.physical_abilities]

    def get_physical_abilities(self):
        abilities = {}
        for node in self.bodypart_tree.nodes:
            for ability_name, ability_value in node.instance.physical_abilities.iteritems():
                if ability_name not in abilities:
                    abilities[ability_name] = ability_value
                else:
                    if abilities[ability_name] < ability_value:
                        abilities[ability_name] = ability_value

        return abilities
