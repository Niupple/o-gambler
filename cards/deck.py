import random
from engineering.exceptions import NotEnoughCardExeption

class Deck:
    def __init__(self, lst : list):
        self._deck = lst

    def shuffle(self):
        random.shuffle(self._deck)

    def deal(self, count=1):
        if count < 0:
            raise NotEnoughCardExeption
        elif count > len(self._deck):
            raise NotEnoughCardExeption
        else:
            ret, self._deck = self._deck[:count], self._deck[count:]
            return ret
