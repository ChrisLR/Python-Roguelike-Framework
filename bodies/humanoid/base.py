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

    template_torso = bodyparts.HumanoidTorso
    template_heart = bodyparts.HumanoidHeart
    template_lungs = bodyparts.HumanoidLungs

    template_neck = bodyparts.HumanoidNeck
    template_head = bodyparts.HumanoidHead
    template_brain = bodyparts.HumanoidBrain
    template_left_eye = bodyparts.HumanoidEye
    template_right_eye = bodyparts.HumanoidEye
    template_left_ear = bodyparts.HumanoidEar
    template_right_ear = bodyparts.HumanoidEar
    template_mouth = bodyparts.HumanoidMouth
    template_teeth = bodyparts.HumanoidTeeth
    template_nose = bodyparts.HumanoidNose

    template_left_arm = bodyparts.HumanoidArm
    template_left_hand = bodyparts.HumanoidHand
    template_right_arm = bodyparts.HumanoidArm
    template_right_hand = bodyparts.HumanoidHand

    template_left_leg = bodyparts.HumanoidLeg
    template_left_foot = bodyparts.HumanoidFoot
    template_right_leg = bodyparts.HumanoidLeg
    template_right_foot = bodyparts.HumanoidFoot

    def __init__(self):
        self.torso = self.template_torso(self.name, "")
        self.heart = self.template_heart(self.name, "", inserted_in=self.torso)
        self.lungs = self.template_lungs(self.name, "", inserted_in=self.torso)

        self.neck = self.template_neck(self.name, "", attached_to=self.torso)
        self.head = self.template_head(self.name, "", attached_to=self.neck)
        self.brain = self.template_brain(self.name, "", inserted_in=self.head)
        self.left_eye = self.template_left_eye(self.name, "left", inserted_in=self.head)
        self.right_eye = self.template_right_eye(self.name, "right", inserted_in=self.head)
        self.left_ear = self.template_left_ear(self.name, "left", attached_to=self.head)
        self.right_ear = self.template_right_ear(self.name, "left", attached_to=self.head)
        self.mouth = self.template_mouth(self.name, "", inserted_in=self.head)
        self.teeth = self.template_teeth(self.name, "", inserted_in=self.mouth)
        self.nose = self.template_nose(self.name, "", attached_to=self.head)

        self.left_arm = self.template_left_arm(self.name, "left", attached_to=self.torso)
        self.left_hand = self.template_left_hand(self.name, "left", attached_to=self.left_arm)
        self.right_arm = self.template_right_arm(self.name, "right", attached_to=self.torso)
        self.right_hand = self.template_right_hand(self.name, "right", attached_to=self.right_arm)

        self.left_leg = self.template_left_leg(self.name, "left", attached_to=self.torso)
        self.left_foot = self.template_left_foot(self.name, "left", attached_to=self.left_leg)
        self.right_leg = self.template_right_leg(self.name, "right", attached_to=self.torso)
        self.right_foot = self.template_right_foot(self.name, "right", attached_to=self.right_leg)

        super().__init__(
            (
                self.torso, self.heart, self.lungs,
                self.neck, self.head, self.brain,
                self.nose, self.left_ear, self.right_ear,
                self.left_eye, self.right_eye,
                self.left_arm, self.left_hand,
                self.right_arm, self.right_hand,
                self.left_leg, self.left_foot,
                self.right_leg, self.right_foot,
                self.teeth,
            )
        )
