from proficiencies.base import Proficiency


class WeaponProficiency(Proficiency):
    pass


class Javelin(WeaponProficiency):
    uid = "javelin"
    name = "Javelin"


class GreatAxe(WeaponProficiency):
    uid = "great_axe"
    name = "Great Axe"
