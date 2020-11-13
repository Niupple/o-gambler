from .abstract_cards import AbstractCardSet
from .suits import SPADE, HEART, CLUB, DIAMOND
from .suits import symbol as suit_symbol
from .points import symbol as point_symbol
from .deck import Deck

class PokerCard:
    def __init__(self, params):
        point, suit, joker = params
        self.point = point
        self.suit = suit
        self.joker = joker

    def __str__(self):
        if self.joker == 0:
            return 'joker'
        elif self.joker == 1:
            return 'JOKER'
        else:
            return point_symbol[self.point] + suit_symbol[self.suit]

class ClassicPokerSet(AbstractCardSet):
    def __init__(self):
        super().__init__()
        self._list = self.__reconstruct()

    def __reconstruct(self):
        lst = []
        for i in range(13):
            lst.append((i, SPADE, None))
            lst.append((i, HEART, None))
            lst.append((i, CLUB, None))
            lst.append((i, DIAMOND, None))
        lst.append((None, None, 0))
        lst.append((None, None, 1))
        return list(map(PokerCard, lst))

    def get_deck(self):
        return Deck(self._list)

class ClassicTexasHoldemSet(AbstractCardSet):
    def __init__(self):
        super().__init__()
        self._list = self.__reconstruct()

    def __reconstruct(self):
        lst = []
        for i in range(13):
            lst.append((i, SPADE, None))
            lst.append((i, HEART, None))
            lst.append((i, CLUB, None))
            lst.append((i, DIAMOND, None))
        return list(map(PokerCard, lst))

    def get_deck(self):
        return Deck(self._list)
