from bodies.body_part_tree import BodypartTree
import bodyparts
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

    humanoid_tree = BodypartTree(bodyparts.HumanoidTorso)
    humanoid_tree.insert(bodyparts.HumanoidTorso, bodyparts.HumanoidHeart)
    humanoid_tree.insert(bodyparts.HumanoidTorso, bodyparts.HumanoidLungs)
    humanoid_tree.attach(bodyparts.HumanoidTorso, bodyparts.HumanoidHead)
    humanoid_tree.attach(bodyparts.HumanoidHead, 'left eye', 'humanoid_eye')
    humanoid_tree.attach(bodyparts.HumanoidHead, 'right eye', 'humanoid_eye')
    humanoid_tree.attach(bodyparts.HumanoidHead, 'left ear', 'humanoid_ear')
    humanoid_tree.attach(bodyparts.HumanoidHead, 'right ear', 'humanoid_ear')
    humanoid_tree.attach(bodyparts.HumanoidHead, 'mouth', 'humanoid_mouth')
    humanoid_tree.insert(bodyparts.HumanoidHead, 'brain', 'humanoid_brain')
    humanoid_tree.attach(bodyparts.HumanoidTorso, 'left arm', 'humanoid_arm')
    humanoid_tree.attach('left arm', 'left hand', 'humanoid_hand')
    humanoid_tree.attach(bodyparts.HumanoidTorso, 'right arm', 'humanoid_arm')
    humanoid_tree.attach('right arm', 'right hand', 'humanoid_hand')
    humanoid_tree.attach(bodyparts.HumanoidTorso, 'left leg', 'humanoid_leg')
    humanoid_tree.attach('left leg', 'left foot', 'humanoid_foot')
    humanoid_tree.attach(bodyparts.HumanoidTorso, 'right leg', 'humanoid_leg')
    humanoid_tree.attach('right leg', 'right foot', 'humanoid_foot')

    return humanoid_tree
