class Value(object):
    UNKNOWN = 0
    WIN = 1
    TIE = 2
    LOSS = 3
    values = ['UNKNOWN', 'WIN', 'TIE', 'LOSS']

    @classmethod
    def print_value(cls, value):
        print cls.values[value]
