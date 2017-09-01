class EchoService(object):
    singleton = None

    def __init__(self, console, game_context):
        self.console = console
        self.game_context = game_context
        EchoService.singleton = self

    def echo(self, message, context=None):
        if context:
            replaced_message = context.replace(message)
            self.console.add_lines(replaced_message + "\n")
        else:
            self.console.add_lines(message + "\n")

    def player_echo(self, actor, message, context=None):
        if actor.is_player:
            self.echo(message, context)
