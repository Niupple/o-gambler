from .abstract_cards import AbstractCardSet
from .suits import SPADE, HEART, CLUB, DIAMOND

class PokerCard:
    def __init__(self, params):
        point, suit, joker = params
        self.point = point
        self.suit = suit
        self.joker = joker

class ClassicPokerSet(AbstractCardSet):
    def __init__(self):
        super().__init__(self)
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
        return list(map(PokerCard.__init__, lst))
