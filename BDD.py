import networkx as nx
from matplotlib import pyplot as plt

def genid():
    i = 2
    while True:
        yield i
        i += 1

ids = genid()

class BDD:
    def __init__(self, x, neg=None, pos=None):
        self.x = x
        self.neg = neg
        self.pos = pos
        if self.x == 0:
            self.id = 0
        if self.x == 1:
            self.id = 1
        else:
            self.id = next(ids)

    def lor(self, other):
        if self.x == 0:
            return other
        if self.x == 1:
            return ONE
        if other.x == 0:
            return self
        if other.x == 1:
            return ONE
        if self.x == other.x:
            return BDD(self.x, self.neg.lor(other.neg), self.pos.lor(other.pos))
        if self.x > other.x:
            return BDD(self.x, self.neg.lor(other), self.pos.lor(other))
        return BDD(other.x, self.lor(other.neg), self.lor(other.pos))

    def land(self, other):
        if self.x == 0:
            return ZERO
        if self.x == 1:
            return other
        if other.x == 0:
            return ZERO
        if other.x == 1:
            return self
        if self.x == other.x:
            return BDD(self.x, self.neg.land(other.neg), self.pos.land(other.pos))
        if self.x > other.x:
            return BDD(self.x, self.neg.land(other), self.pos.land(other))
        return BDD(other.x, self.land(other.neg), self.land(other.pos))

    def print(self, d=0):
        if self.x == 0:
            print(" "*d, "zero")
        elif self.x == 1:
            print(" "*d, "one")
        else:
            self.pos.print(d+2)
            print(" "*d, self.x)
            self.neg.print(d+2)

    def nodes(self):
        if self.x == 0:
            return [(self.id, self.x)]
        if self.x == 1:
            return [(self.id, self.x)]
        return [(self.id, self.x)] + self.neg.nodes() + self.pos.nodes()

    def posedges(self):
        if self.x == 0:
            return []
        if self.x == 1:
            return []
        return [(self.id, self.pos.id)] + self.neg.posedges() + self.pos.posedges()

    def negedges(self):
        if self.x == 0:
            return []
        if self.x == 1:
            return []
        return [(self.id, self.neg.id)] + self.neg.negedges() + self.pos.negedges()


