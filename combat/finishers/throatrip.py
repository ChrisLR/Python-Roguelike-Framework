from combat import attacks
from combat.finishers.base import Finisher
from echo import functions
from util import gridhelpers


class ThroatRip(Finisher):
    name = "Throat Rip"
    description = "Rip your enemy's throat apart with your fangs"
    attacker_message = "You savagely rip into {defender_his} throat with your fangs " \
                       "until {defender_he} stops moving."

    observer_message = "{attacker} savagely rips into {defender_his} throat with {attacker_his} fangs " \
                       "until {defender_he} stops moving."

    @classmethod
    def evaluate(cls, attack_result):
        if attack_result.context.distance_to <= 1:
            if attack_result.context.attack_used == attacks.Bite:
                return True
        return False

    @classmethod
    def execute(cls, attack_result):
        return cls.get_message(attack_result)

    @classmethod
    def get_message(cls, attack_result):
        attacker = attack_result.context.attacker
        defender = attack_result.context.defender
        if attack_result.context.attacker.is_player:
            return cls.attacker_message.format(
                defender_his=functions.his_her_it(defender),
                defender_he=functions.he_her_it(defender),
            )
        else:
            return cls.observer_message.format(
                attacker=functions.get_name_or_string(attacker),
                defender_his=functions.his_her_it(defender),
                attacker_his=functions.his_her_it(attacker),
                attacker_he=functions.he_her_it(attacker),
                defender_he=functions.he_her_it(defender)
            )
