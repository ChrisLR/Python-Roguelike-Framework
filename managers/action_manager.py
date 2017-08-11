from characters import actions


class ActionManager(object):
    def __init__(self):
        pass

    def move_or_attack(self, player, key_x, key_y):
        actions.move_or_attack(player, key_x, key_y)

    def monster_take_turn(self, monster, player):
        actions.monster_take_turn(monster, player)
