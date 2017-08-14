class EchoService(object):
    singleton = None

    def __init__(self, console, game_context):
        self.console = console
        self.game_context = game_context
        EchoService.singleton = self

    def echo(self, message, context=None):
        if "{attacker_his}" in message:
            print("Hm")
        if context:
            replaced_message = context.replace(message)
            self.console.add_lines(replaced_message + "\n")
        else:
            # DEBUG REMOVE THIS
            if "{" in message:
                raise ValueError("PROVIDED NO CONTEXT BUT SHOULD.")
            self.console.add_lines(message + "\n")
