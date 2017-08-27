from bodies.humanoid import HumanoidBody
from data.python_templates import material
import bodyparts


class DraconianBody(HumanoidBody):
    uid = "draconian"
    name = "Draconian"

    template_outer_material = material.DragonScale
    template_left_hand = bodyparts.DraconianHand
    template_right_hand = bodyparts.DraconianHand
    template_left_foot = bodyparts.DraconianFoot
    template_right_foot = bodyparts.DraconianFoot
    template_teeth = bodyparts.DraconianTeeth

    template_muzzle = bodyparts.DraconianMuzzle
    template_tail = bodyparts.DraconianTail

    def __init__(self):
        super().__init__()
        self.muzzle = self.template_muzzle(self.name, "", attached_to=self.head)
        self.tail = self.template_tail(self.name, "", attached_to=self.torso)
        self.bodyparts += (
            self.muzzle,
            self.tail,
        )
