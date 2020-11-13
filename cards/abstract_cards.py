import random

class AbstractCardSet:
    def __init__(self):
        self._list = []

    def __len__(self):
        return len(self._list)

    def shuffle(self, len=-1):
        # to construct a deck of cards
        raise NotImplementedError
