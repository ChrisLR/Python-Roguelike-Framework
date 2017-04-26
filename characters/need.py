class Need(object):
    def __init__(self, name, positive_threshold_messages, negative_threshold_messages, threshold_effects):
        """
        For use with the needs component.
        :param name: Name of the NEED.
        :param positive_threshold_messages: int:str Percentage as key and positive message as value.
        :param negative_threshold_messages: int:str Percentage as key and negative message as value.
        :param threshold_effects: int:effect Percentage as key and negative effect to apply as value.
        """
        self.name = name
        self.positive_threshold_messages = positive_threshold_messages
        self.negative_threshold_messages = negative_threshold_messages
        self.threshold_effects = threshold_effects
