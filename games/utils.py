def get_frequency_no_suits(hand : set):
    ret = [0 for i in range(15)]
    for card in hand:
        if card.joker is None:
            ret[card.point] += 1
        else:
            ret[13 + card.joker] += 1
    return ret

def get_frequency_by_suits(hand : set):
    ret = [[0 for i in range(15)] for j in range(4)]
    for card in hand:
        if card.joker is None:
            ret[card.suit][card.point] += 1
        else:
            ret[0][13 + card.joker] += 1
    return ret

def get_frequency_in_suits(hand : set):
    ret = [[] for i in range(15)]
    for card in hand:
        if card.joker is None:
            ret[card.point].append(card.suit)
        else:
            ret[13 + card.joker].append(0)
    return ret

def shape_contains(freq_hand : list, shape : list):
    freq_shape = [0 for i in range(15)]
    for card in shape:
        freq_shape[card] += 1
    for i in range(15):
        if freq_shape[i] > freq_hand[i]:
            return False
    return True

def shape_equals(freq_hand : list, shape : list):
    freq_shape = [0 for i in range(15)]
    for card in shape:
        freq_shape[card] += 1
    for i in range(15):
        if freq_shape[i] != freq_hand[i]:
            return False
    return True

def powersets(s : list):
    l = len(s)
    for i in range(1<<l):
        ret = []
        x = i
        cnt = 0
        while x != 0:
            if x&1 != 0:
                ret.append(s[cnt])
            cnt += 1
            x >>= 1
        yield ret[:]

if __name__ == "__main__":
    print("hello")
    lst = [1, 2, 3]
    for s in powersets(lst):
        print(s)
