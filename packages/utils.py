class Value(object):
    UNKNOWN = 0
    WIN = 1
    TIE = 2
    LOSS = 3
    # Special case...a draw is what we have left over as unkown when done solving a game
    DRAW = 0
    values = ['DRAW', 'WIN', 'TIE', 'LOSS']

    @classmethod
    def print_value(cls, value):
        print cls.values[value]
