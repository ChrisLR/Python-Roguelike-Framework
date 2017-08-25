from bodies.body_part_tree import BodypartTree
from bodies.blood.base import Blood
from components.body import Body
from data.python_templates import material


class HumanoidBody(Body):
    uid = "humanoid"
    name = "Humanoid"
    base_height = 5
    base_weight = 150

    template_blood = Blood
    template_structural_material = material.Bone
    template_inner_material = material.Flesh
    template_outer_material = material.Skin
    template_bodypart_tree = build_humanoid_body_part_tree()


def build_humanoid_body_part_tree():
    humanoid_tree = BodypartTree('torso', 'humanoid_torso')
    humanoid_tree.insert('torso', 'heart', 'humanoid_heart')
    humanoid_tree.insert('torso', 'lungs', 'humanoid_lungs')
    humanoid_tree.attach('torso', 'head', 'humanoid_head')
    humanoid_tree.attach('head', 'left eye', 'humanoid_eye')
    humanoid_tree.attach('head', 'right eye', 'humanoid_eye')
    humanoid_tree.attach('head', 'left ear', 'humanoid_ear')
    humanoid_tree.attach('head', 'right ear', 'humanoid_ear')
    humanoid_tree.attach('head', 'mouth', 'humanoid_mouth')
    humanoid_tree.insert('head', 'brain', 'humanoid_brain')
    humanoid_tree.attach('torso', 'left arm', 'humanoid_arm')
    humanoid_tree.attach('left arm', 'left hand', 'humanoid_hand')
    humanoid_tree.attach('torso', 'right arm', 'humanoid_arm')
    humanoid_tree.attach('right arm', 'right hand', 'humanoid_hand')
    humanoid_tree.attach('torso', 'left leg', 'humanoid_leg')
    humanoid_tree.attach('left leg', 'left foot', 'humanoid_foot')
    humanoid_tree.attach('torso', 'right leg', 'humanoid_leg')
    humanoid_tree.attach('right leg', 'right foot', 'humanoid_foot')

    return humanoid_tree
