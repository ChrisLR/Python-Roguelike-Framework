from bodies.humanoid import HumanoidBody
import bodyparts
from data.python_templates import material


class TrollishBody(HumanoidBody):
    uid = "trollish"
    name = "Trollish"

    template_outer_material = material.Hide

    template_left_hand = bodyparts.TrollishHand
    template_right_hand = bodyparts.TrollishHand
    template_teeth = bodyparts.TrollishFangs
