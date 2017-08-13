from characters import actions


class ActionManager(object):
    def __init__(self, game_context):
        self.game_context = game_context

    def move_or_attack(self, player, key_x, key_y):
        actions.move_or_attack(player, key_x, key_y, self.game_context)

    def monster_take_turn(self, monster, player):
        actions.monster_take_turn(monster, player, self.game_context)
