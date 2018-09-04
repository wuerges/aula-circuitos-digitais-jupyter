import networkx as nx
#from matplotlib import pyplot as plt
import pydot
from IPython.display import Image

def plotbdd(bdd):
    G = pydot.Dot()
    G.set_type("digraph")
    for (i, x) in bdd.nodes():
        if x == 0:
            G.add_node(pydot.Node(str(i), label=str(x), shape="rectangle", color="red"))
        if x == 1:
            G.add_node(pydot.Node(str(i), label=str(x), shape="rectangle", color="blue"))
        else:
            G.add_node(pydot.Node(str(i), label=str(x)))

    for (a,b) in bdd.posedges():
        G.add_edge(pydot.Edge(str(a), str(b), color='blue'))
    for (a,b) in bdd.negedges():
        G.add_edge(pydot.Edge(str(a), str(b), color='red'))

    display(Image(G.create(prog='dot', format='png')))


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

    def remove_identical(self, keep):
        k = (self.x, self.pos.id, self.neg.id)
        ret = self
        if k in keep:
            ret = keep[k]
        if ret.x != 0 and ret.x != 1:
            ret.pos = ret.pos.remove_identical(keep)
            ret.neg = ret.neg.remove_identical(keep)
        return ret

    def get_item(self):
        return ((self.x, self.pos.id, self.neg.id), self)

    def get_items(self):
        if self.x == 0 or self.x == 1:
            return [self.get_item()]
        return [self.get_item()] + self.neg.get_items() + self.pos.get_items()

    def simplify_identical(self):
        keep = dict(self.get_items())
        return self.remove_identical(keep)

    def remove_redundant(self):
        if self.id == 0 or self.id == 1:
            return False, self
        rpos, self.pos = self.pos.remove_redundant()
        rneg, self.neg = self.neg.remove_redundant()
        if self.pos.id == self.neg.id:
            return True, self.pos
        return rpos or rneg

    def simplify(self):
        x = self
        r = True
        while r:
            x = x.simplify_identical()
            r, x = x.remove_redundant()

        return x

ZERO = BDD(0)
ZERO.neg = ZERO
ZERO.pos = ZERO

ONE = BDD(1)
ONE.neg = ONE
ONE.pos = ONE
