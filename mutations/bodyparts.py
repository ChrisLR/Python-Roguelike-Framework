from mutations.base import Mutation
from managers.echo import EchoService
from echo import functions


class BodypartsMutation(Mutation):
    """
    A mutation targeting a base body part type turning into equivalent mutated_body_part.
    """
    name = "Bodypart Mutation"
    example_message = "{actor}"

    def __init__(self, base_body_part_type, mutated_body_part_type, apply_message, revert_message,affect_all=False):
        """
        :param base_body_part_type: Base body part type
        :param mutated_body_part_type:  mutated body part type
        :param apply_message: String containing tag {actor} to echo on apply.
        :param revert_message: String containing tag {actor} to echo on revert.
        :param affect_all: If true, will replace every body part corresponding to the base body part type.
        """
        self.base_body_part_type = base_body_part_type
        self.mutated_body_part_type = mutated_body_part_type
        self.apply_message = apply_message
        self.revert_message = revert_message
        self.affect_all = affect_all
        self.swapped_body_parts = []

    def apply(self, actor):
        body = actor.body
        if self.affect_all:
            old_body_parts = body.get_body_parts(self.base_body_part_type.uid)
        else:
            old_body_parts = (body.get_body_part(self.base_body_part_type.uid),)

        if not old_body_parts:
            return

        EchoService.singleton.echo(self.apply_message.format(actor=functions.names_or_your(actor)))
        for old_body_part in old_body_parts:
            new_body_part = self.mutated_body_part_type()
            body.replace_body_part(old_body_part, new_body_part)
            self.swapped_body_parts.append((old_body_part, new_body_part))

    def revert(self, actor):
        body = actor.body
        if not self.swapped_body_parts:
            return
        
        for old_body_part, new_body_part in self.swapped_body_parts:
            body.replace_body_part(new_body_part, old_body_part)
        EchoService.singleton.echo(self.revert_message.format(actor=functions.names_or_your(actor)))
