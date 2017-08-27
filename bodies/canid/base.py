import bodyparts
from bodies.blood.base import Blood
from components.body import Body
from data.python_templates import material


class CanidBody(Body):
    uid = "canid"
    name = "Canid"
    base_height = 3
    base_weight = 50

    template_blood = Blood
    template_structural_material = material.Bone
    template_inner_material = material.Flesh
    template_outer_material = material.Fur

    template_torso = bodyparts.CanidTorso
    template_heart = bodyparts.CanidHeart
    template_lungs = bodyparts.CanidLungs

    template_neck = bodyparts.CanidNeck
    template_head = bodyparts.CanidHead
    template_brain = bodyparts.CanidBrain
    template_left_eye = bodyparts.CanidEye
    template_right_eye = bodyparts.CanidEye
    template_left_ear = bodyparts.CanidEar
    template_right_ear = bodyparts.CanidEar
    template_muzzle = bodyparts.CanidMuzzle
    template_fangs = bodyparts.CanidFangs
    template_nose = bodyparts.CanidNose

    template_left_foreleg = bodyparts.CanidForeleg
    template_left_fore_paw = bodyparts.CanidPaw
    template_right_foreleg = bodyparts.CanidForeleg
    template_right_fore_paw = bodyparts.CanidPaw

    template_left_hind_leg = bodyparts.CanidHindLeg
    template_left_hind_paw = bodyparts.CanidPaw
    template_right_hind_leg = bodyparts.CanidHindLeg
    template_right_hind_paw = bodyparts.CanidPaw

    template_tail = bodyparts.CanidTail

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
        self.muzzle = self.template_muzzle(self.name, "", attached_to=self.head)
        self.fangs = self.template_fangs(self.name, "", inserted_in=self.muzzle)
        self.nose = self.template_nose(self.name, "", attached_to=self.head)

        self.left_foreleg = self.template_left_foreleg(self.name, "left", attached_to=self.torso)
        self.left_fore_paw = self.template_left_fore_paw(self.name, "left fore", attached_to=self.left_foreleg)
        self.right_foreleg = self.template_right_foreleg(self.name, "right", attached_to=self.torso)
        self.right_fore_paw = self.template_right_fore_paw(self.name, "right fore", attached_to=self.right_foreleg)

        self.left_hind_leg = self.template_left_hind_leg(self.name, "left", attached_to=self.torso)
        self.left_hind_paw = self.template_left_hind_paw(self.name, "left hind", attached_to=self.left_hind_leg)
        self.right_hind_leg = self.template_right_hind_leg(self.name, "right", attached_to=self.torso)
        self.right_hind_paw = self.template_right_hind_paw(self.name, "right hind", attached_to=self.right_hind_leg)

        self.tail = self.template_tail(self.name, "", attached_to=self.torso)

        super().__init__(
            (
                self.torso, self.heart, self.lungs,
                self.neck, self.head, self.brain,
                self.left_eye, self.right_eye,
                self.left_ear, self.right_ear,
                self.muzzle, self.fangs, self.nose,
                self.left_foreleg, self.left_fore_paw,
                self.right_foreleg, self.right_fore_paw,
                self.left_hind_leg, self.left_hind_paw,
                self.right_hind_leg, self.right_hind_paw,
                self.tail,
            )
        )
