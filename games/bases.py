from .utils import powersets

class Shape:
    def __init__(self):
        pass

    @classmethod
    def get_high(cls, hand : set):
        high = None
        for comb in cls.get_all(hand):
            if comb >= high:
                high = comb
        return high

    @classmethod
    def get_all(cls, hand : set):
        for h in powersets(list(hand)):
            obj = cls.match(h)
            if obj is not None:
                yield obj

    @classmethod
    def match(cls, hand : set):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def __lt__(self, rhs):
        raise NotImplementedError

    def __gt__(self, rhs):
        if not isinstance(rhs, type(self)):
            raise TypeError
        return rhs < self

    def __le__(self, rhs):
        if not isinstance(rhs, type(self)):
            raise TypeError
        return not (rhs < self)

    def __ge__(self, rhs):
        if not isinstance(rhs, type(self)):
            raise TypeError
        return not (self < rhs)

    def __eq__(self, rhs):
        if not isinstance(rhs, type(self)):
            raise TypeError
        return not (self < rhs) and not (rhs < self)

    def __ne__(self, rhs):
        if not isinstance(rhs, type(self)):
            raise TypeError
        return not self == rhs
