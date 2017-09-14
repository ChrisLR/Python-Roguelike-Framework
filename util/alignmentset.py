class AlignmentSet(object):
    """
    This is the preferred alignments, True means Preferred, None is Neutral, False is Shunned
    """
    __slots__ = ["law", "chaos", "good", "evil"]

    def __init__(self, law=None, chaos=None, good=None, evil=None):
        self.law = law
        self.chaos = chaos
        self.good = good
        self.evil = evil
