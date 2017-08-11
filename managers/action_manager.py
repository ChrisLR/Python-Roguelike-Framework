from characters import actions


class ActionManager(object):
    def __init__(self, game_context):
        self.game_context = game_context

    def move_or_attack(self, player, key_x, key_y, game_context):
        actions.move_or_attack(player, key_x, key_y, game_context)

    def monster_take_turn(self, monster, player, game_context):
        actions.monster_take_turn(monster, player, game_context)
