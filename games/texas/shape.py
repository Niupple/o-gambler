from games.bases import Shape
from games.utils import get_frequency_by_suits, get_frequency_no_suits, get_frequency_in_suits, shape_contains, shape_equals
from cards.points import pA, pK, pQ, pJ, p10
from .concept import CardOrder

def getCombs(freq, *counts):
    if len(counts) == 0:
        for i in range(13):
            if len(freq[i]) != 0:
                return None
        return []
    for i in range(13):
        if len(freq[i]) == counts[0]:
            cards = freq[i]
            freq[i] = []
            ret = getCombs(freq, counts[1:])
            if ret is None:
                return ret
            else:
                return [[(i, suit) for suit in cards], *ret]
    return None

class RoyalStraightFlush(Shape):
    def __init__(self, suit):
        super().__init__(self)
        self.suit = suit

    @classmethod
    def match(cls, hand : set):
        freq = get_frequency_by_suits(hand)
        for i in range(4):
            if shape_equals(freq[i], [pA, pK, pQ, pJ, p10]):
                return cls(i)
        return None

    def __lt__(self, rhs):
        if not isinstance(rhs, RoyalStraightFlush):
            raise TypeError
        return False

class StraightFlush(Shape):
    def __init__(self, suit, high):
        super().__init__(self)
        self.suit = suit
        self.high = high

    @classmethod
    def match(cls, hand : set):
        freq = get_frequency_by_suits(hand)
        for i in range(4):
            if shape_equals(freq[i], [pA, pK, pQ, pJ, p10]):
                return cls(i, pA)
            for j in range(9):
                if shape_equals(freq[i], [k for k in range(j, j+5)]):
                    return cls(i, j+4)
        return None

    def __lt__(self, rhs : StraightFlush):
        if not isinstance(rhs, RoyalStraightFlush):
            raise TypeError
        return CardOrder.compare(self.high, rhs.high) < 0

class FourOfAKind(Shape):
    def __init__(self, main, suit_kick, kick):
        super().__init__(self)
        self.main = main
        self.suit_kick = suit_kick
        self.kick = kick

    @classmethod
    def match(cls, hand : set):
        freq = get_frequency_in_suits(hand)
        ret = getCombs(freq, 4, 1)
        if ret is None:
            return ret
        else:
            return cls(ret[0][0][0], ret[1][0][1], ret[1][0][0])
        return None

    def __lt__(self, rhs : FourOfAKind):
        if not isinstance(rhs, FourOfAKind):
            raise TypeError
        return CardOrder.compare([self.main, self.kick], [rhs.main, rhs.kick]) < 0

class FullHouse(Shape):
    def __init__(self, three, two):
        super().__init__(self)
        self.three = three
        self.two = two

    @classmethod
    def match(cls, hand : set):
        freq = get_frequency_in_suits(hand)
        ret = getCombs(freq, 3, 2)
        if ret is None:
            return ret
        else:
            return cls(freq[0], freq[1])

    def __lt__(self, rhs : FullHouse):
        if not isinstance(rhs, FullHouse):
            raise TypeError
        return CardOrder.compare([self.three[0][0], self.two[0][0]], [rhs.three[0][0], rhs.two[0][0]]) < 0

class Flush:
    def __init__(self, suit, points):
        super().__init__(self)
        self.suit = suit
        self.points = sorted(points, lambda x : -x)

    @classmethod
    def match(cls, hand : set):
        if len(hand) != 5:
            return None
        suit = None
        points = []
        for card in hand:
            if suit is None:
                suit = card.suit
                points.append(card.point)
            elif suit != card.suit:
                return None
            else:
                points.append(card.point)
        return cls(suit, points)

    def __lt__(self, rhs : Flush):
        if not isinstance(rhs, FullHouse):
            raise TypeError
        return CardOrder.compare(self.points, rhs.points) < 0

class Straight(Shape):
    def __init__(self, high, suits):
        super().__init__(self)
        self.high = high
        self.suits = suits

    @classmethod
    def match(cls, hand : set):
        if len(hand) != 5:
            return False
        freq = get_frequency_in_suits(hand)
        cnt = 0
        suits = []
        if len(freq[pA]) == len(freq[pK]) == len(freq[pQ]) == len(freq[pJ]) == len(freq[p10]):
            return cls(pA, [freq[p10][0], freq[pJ][0], freq[pQ][0], freq[pK][0], freq[pA][0]])
        for i in range(13):
            if len(freq[i]) == 0:
                if cnt == 5:
                    return cls(i, suits)
                cnt = 0
                suits = []
            elif len(freq[i]) == 1:
                cnt += 1
                suits.append(freq[i][0])
            else:
                return None
        return None

    def __lt__(self, rhs : Flush):
        if not isinstance(rhs, Flush):
            raise TypeError
        return CardOrder.compare(self.high, rhs.high) < 0

class ThreeOfAKind(Shape):
    def __init__(self, three, a, b):
        super().__init__(self)
        self.three = three
        self.kick_a = a
        self.kick_b = b
        if CardOrder.compare(self.kick_a[0], self.kick_b[0]) < 0:
            self.kick_a, self.kick_b = self.kick_b, self.kick_a

    @classmethod
    def match(cls, hand : set):
        freq = get_frequency_in_suits(hand)
        ret = getCombs(freq, 3, 1, 1)
        if ret is None:
            return None
        else:
            return cls(ret[0], ret[1][0], ret[2][0])

    def __lt__(self, rhs : ThreeOfAKind):
        if not isinstance(rhs, ThreeOfAKind):
            raise TypeError
        return CardOrder.compare([self.three[0][0], self.kick_a[0], self.kick_b[0]], [rhs.three[0][0], rhs.kick_a[0], rhs.kick_b[0]]) < 0

class TwoPairs(Shape):
    def __init__(self, a, b, kick):
        super().__init__(self)
        self.kick = kick
        if a[0][0] < b[0][0]:
            a, b = b, a
        self.pair_a = a
        self.pair_b = b

    @classmethod
    def match(cls, hand : set):
        freq = get_frequency_in_suits(hand)
        ret = getCombs(freq, 2, 2, 1)
        if ret is None:
            return None
        else:
            return cls(ret[0], ret[1], ret[2][0])

    def __lt__(self, rhs : TwoPairs):
        if not isinstance(rhs, TwoPairs):
            raise TypeError
        return CardOrder.compare([self.pair_a[0][0], self.pair_b[0][0], self.kick[0]], [rhs.pair_a[0][0], self.pair_b[0][0], self.kick[0]]) < 0

class Pair(Shape):
    def __init__(self, pair, kicks):
        super().__init__(self)
        self.pair = pair
        self.kicks = sorted(kicks, key=lambda x : -x[0])

    @classmethod
    def match(cls, hand : set):
        freq = get_frequency_in_suits(hand)
        ret = getCombs(freq, 2, 1, 1, 1)
        if ret is None:
            return None
        else:
            return cls(ret[0], ret[1:])

    def __lt__(self, rhs : Pair):
        if not isinstance(rhs, Pair):
            raise TypeError
        return CardOrder.compare([self.pair[0][0], self.kicks[0][0], self.kicks[1][0], self.kicks[2][0]], [rhs.pair[0][0], rhs.kicks[0][0], rhs.kicks[1][0], rhs.kicks[2][0]]) < 0

class Highcard(Shape):
    def __init__(self, cards):
        super().__init__(self)
        self.cards = sorted(cards, key=lambda x : -x[0])

    @classmethod
    def match(cls, hand : set):
        freq = get_frequency_in_suits(hand)
        ret = getCombs(freq, 1, 1, 1, 1, 1)
        if ret is None:
            return None
        else:
            return cls(ret)

    def __lt__(self, rhs : Highcard):
        return CardOrder.compare(list(map(lambda x:x[0], self.cards)), list(map(lambda x:x[0], rhs.cards))) < 0

if __name__ == "__main__":
    pass

