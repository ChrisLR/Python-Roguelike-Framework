from combat.attacks.base import Attack
from combat import targets
from combat.enums import DamageType


class MeleeAttack(Attack):
    name = "Melee Attack"
    target_type = targets.Single
    description = "Basic attack for any weapons."

    @classmethod
    def execute(cls, actor, target):
        weapons = cls.get_used_weapons(actor)
        pass

    @classmethod
    def get_used_weapons(cls, attacker):
        """
        This Method will return the real wielded weapons.
        If none it will return anything that is wielded (Improvised Weapon)
        :param attacker: GameObject that is attacking
        :return: List of Items or None
        """
        items = attacker.equipment.get_wielded_items()
        weapons = [item for item in items if item.weapon]

        if weapons:
            return weapons
        else:
            return items

    @classmethod
    def get_melee_damage_type(cls, item):
        if item.weapon:
            return item.weapon.melee_damage_type
        else:
            return DamageType.Blunt


    def get_hit_bonus(self, attacker, **kwargs):
        return self.modifiers.get('hit_modifier', 0) + attacker.get_stat_modifier(self.hit_stat_used)

    def get_damage_bonus(self, attacker, **kwargs):
        return self.modifiers.get('damage_modifier', 0) + attacker.get_stat_modifier(self.damage_stat_used)

    def get_damage_dice(self, **kwargs):
        return DiceStack(1, Dice(1))

    def get_damage_type(self, **kwargs):
        return self.damage_type

    def make_attack(self, attacker, defender, **kwargs):
        attack_result = self.make_hit_roll(attacker, defender, **kwargs)
        if attack_result.success:
            self.make_damage_roll(attacker, attack_result, **kwargs)

        # TODO Probably a good idea to remove this from the attack and into the manager.
        EchoService.singleton.echo(
            message=self.message + "...",
            context=Context.combat(attacker=attacker, defender=defender, **kwargs)
        )
        return attack_result

    def make_hit_roll(self, attacker, defender, **kwargs):
        target_ac = defender.get_armor_class()
        success, critical, natural_roll, total_hit_roll = check_roller.d20_check_roll(
            difficulty_class=target_ac,
            modifiers=self.get_hit_bonus(attacker)
        )
        return AttackResult(success, critical, defender, target_ac, natural_roll, total_hit_roll)

    def make_damage_roll(self, attacker, attack_result, **kwargs):
        total_damage = check_roller.roll_damage(
            dice_stacks=[self.get_damage_dice(**kwargs)],
            modifiers=self.get_damage_bonus(attacker, **kwargs),
            critical=attack_result.critical
        )
        attack_result.total_damage = total_damage
        attack_result.separated_damage = [(total_damage, self.get_damage_type(**kwargs))]

        return attack_result