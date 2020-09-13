class CardOrder:
    @staticmethod
    def get_card_order(card):
        return (card-1)%13

    @staticmethod
    def _compare(lc, rc):
        return CardOrder.get_card_order(lc)-CardOrder.get_card_order(rc)

    @staticmethod
    def compare(lc, rc):
        if not isinstance(lc, list) and not isinstance(rc, list):
            lc = [lc]
            rc = [rc]
        for l, r in zip(lc, rc):
            c = CardOrder._compare(l, r)
            if c != 0:
                return c
        return 0

