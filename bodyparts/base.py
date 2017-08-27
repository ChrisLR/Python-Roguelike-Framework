import abc


class BodyPart(object):
    __metaclass__ = abc.ABCMeta
    __slots__ = [
        "full_name", "short_name",
        "racial_prefix", "positional_prefix", "child_attachments", "child_inserts"
    ]
    base_name = ""

    @abc.abstractclassmethod
    def uid(self):
        pass

    @abc.abstractclassmethod
    def physical_abilities(self):
        pass

    @abc.abstractclassmethod
    def relative_size(self):
        pass

    @abc.abstractclassmethod
    def threat_level(self):
        pass

    @property
    def name(self):
        return self.short_name

    def __init__(self, racial_prefix, positional_prefix, attached_to=None, inserted_in=None):
        self.racial_prefix = racial_prefix
        self.positional_prefix = positional_prefix
        self.full_name = "{} {} {}".format(self.racial_prefix, self.positional_prefix, self.base_name).strip()
        self.short_name = "{} {}".format(self.positional_prefix, self.base_name).strip()
        self.child_attachments = []
        self.child_inserts = []
        if attached_to:
            attached_to.attach(self)
        if inserted_in:
            inserted_in.insert(self)

    def attach(self, child_bodypart):
        self.child_attachments.append(child_bodypart)

    def insert(self, child_bodypart):
        self.child_inserts.append(child_bodypart)


# noinspection PyAbstractClass
class Head(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "head"


# noinspection PyAbstractClass
class Neck(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "neck"


# noinspection PyAbstractClass
class Torso(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "torso"


# noinspection PyAbstractClass
class Arm(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "arm"


# noinspection PyAbstractClass
class Leg(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "leg"


# noinspection PyAbstractClass
class Hand(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "hand"


# noinspection PyAbstractClass
class Foot(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "foot"


# noinspection PyAbstractClass
class Eye(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "eye"


# noinspection PyAbstractClass
class Ear(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "ear"


# noinspection PyAbstractClass
class Mouth(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "mouth"


# noinspection PyAbstractClass
class Muzzle(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "muzzle"


# noinspection PyAbstractClass
class Brain(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "brain"


# noinspection PyAbstractClass
class Heart(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "heart"


# noinspection PyAbstractClass
class Lungs(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "lungs"


# noinspection PyAbstractClass
class Teeth(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "teeth"


# noinspection PyAbstractClass
class Nose(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "nose"


# noinspection PyAbstractClass
class Tail(BodyPart):
    __metaclass__ = abc.ABCMeta
    base_name = "tail"
