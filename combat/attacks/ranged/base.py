from combat.attacks.base import Attack


class RangedAttack(Attack):
    @classmethod
    def get_ranged_weapon(cls, attacker):
        ranged_weapon = next((item for item in attacker.equipment.get_wielded_items()
                              if item.weapon and item.weapon.ranged_damage_type), None)
        return ranged_weapon
