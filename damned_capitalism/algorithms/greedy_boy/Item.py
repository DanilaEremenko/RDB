class Item():
    def __init__(self, id, price, value):
        self.id = id
        self.price = price
        self.value = value
        if price == 0:
            self.k = value
        else:
            self.k = value / price

    def __cmp__(self, other):
        if self.k > other.k:
            return 1
        elif self.k < other.k:
            return -1
        else:
            return 0

    def __gt__(self, other):
        return self.k > other.k
