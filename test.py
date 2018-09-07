from BDD import *


a = BDD('a', ONE, ZERO)
b = BDD('b', ZERO, ONE)
c = BDD('c', ZERO, a.land(b))
plotbdd(c)
